import { useEffect, useMemo, useRef, useState } from "react";
import { APP_SIMULATORS, COLLECTOR_LABELS } from "./content";

const STORAGE_KEY = "behavior-collector-sessions-v1";

const defaultEventFields = {
  x: 0,
  y: 0,
  delta_y: 0,
  velocity: 0,
  acceleration: 0,
  direction: 0,
  pressure: 0,
  duration_ms: 0,
  dwell_before_ms: 0,
  selection_word_count: 0,
};

const buildSessionId = (label) =>
  `web_${label}_${new Date().toISOString().replace(/[-:.TZ]/g, "").slice(0, 14)}`;

const loadStoredSessions = () => {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const downloadJsonl = (events, filename) => {
  const body = events.map((event) => JSON.stringify(event)).join("\n");
  const blob = new Blob([body ? `${body}\n` : ""], { type: "application/jsonl" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
};

const supportsDirectRepoSave = () =>
  typeof window !== "undefined" && typeof window.showDirectoryPicker === "function";

const buildJsonlBody = (events) =>
  events.map((event) => JSON.stringify(event)).join("\n");

function App() {
  const surfaceRef = useRef(null);
  const pointerDownRef = useRef(null);
  const lastScrollRef = useRef({ top: 0, timestamp: 0, velocity: 0 });
  const lastInteractionRef = useRef(0);
  const lastIdleEmitRef = useRef(0);

  const [selectedLabel, setSelectedLabel] = useState(COLLECTOR_LABELS[0]);
  const [sessionId, setSessionId] = useState(() => buildSessionId(COLLECTOR_LABELS[0]));
  const [currentAppId, setCurrentAppId] = useState(APP_SIMULATORS[0].id);
  const [currentPageId, setCurrentPageId] = useState(APP_SIMULATORS[0].pages[0].id);
  const [isRecording, setIsRecording] = useState(false);
  const [currentSessionEvents, setCurrentSessionEvents] = useState([]);
  const [savedSessions, setSavedSessions] = useState(() => loadStoredSessions());
  const [statusMessage, setStatusMessage] = useState(
    "Choose a target label, start recording, switch between simulated apps and pages, then save JSONL into data/raw.",
  );
  const [isSavingToRepo, setIsSavingToRepo] = useState(false);
  const [taskChecks, setTaskChecks] = useState({});

  const currentApp =
    APP_SIMULATORS.find((app) => app.id === currentAppId) ?? APP_SIMULATORS[0];
  const currentPage =
    currentApp.pages.find((page) => page.id === currentPageId) ?? currentApp.pages[0];

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(savedSessions));
  }, [savedSessions]);

  useEffect(() => {
    if (!isRecording) {
      setSessionId(buildSessionId(selectedLabel));
    }
  }, [selectedLabel, isRecording]);

  useEffect(() => {
    const intervalId = window.setInterval(() => {
      if (!isRecording) {
        return;
      }
      const now = Date.now();
      const idleDuration = now - lastInteractionRef.current;
      if (idleDuration < 4500) {
        return;
      }
      if (now - lastIdleEmitRef.current < 3500) {
        return;
      }
      lastIdleEmitRef.current = now;
      recordEvent({
        event_type: "idle",
        duration_ms: idleDuration,
      });
    }, 1000);

    return () => window.clearInterval(intervalId);
  }, [isRecording, selectedLabel, sessionId]);

  const allRecordedEvents = useMemo(
    () => savedSessions.flatMap((session) => session.events),
    [savedSessions],
  );
  const unsavedSessions = useMemo(
    () => savedSessions.filter((session) => !session.repo_saved_at),
    [savedSessions],
  );
  const unsavedRecordedEvents = useMemo(
    () => unsavedSessions.flatMap((session) => session.events),
    [unsavedSessions],
  );

  const totalEventCount = allRecordedEvents.length + currentSessionEvents.length;

  const resetSessionTracking = () => {
    pointerDownRef.current = null;
    lastScrollRef.current = { top: 0, timestamp: 0, velocity: 0 };
    lastInteractionRef.current = Date.now();
    lastIdleEmitRef.current = 0;
    setCurrentSessionEvents([]);
  };

  const recordEvent = (partialEvent) => {
    if (!isRecording) {
      return;
    }

    const timestampMs = Date.now();
    const dwellBeforeMs = lastInteractionRef.current
      ? Math.max(0, timestampMs - lastInteractionRef.current)
      : 0;

    const fullEvent = {
      session_id: sessionId,
      timestamp_ms: timestampMs,
      label: selectedLabel,
      ...defaultEventFields,
      ...partialEvent,
      dwell_before_ms:
        partialEvent.dwell_before_ms !== undefined ? partialEvent.dwell_before_ms : dwellBeforeMs,
    };

    console.log("[behavior-collector] captured event", fullEvent);
    lastInteractionRef.current = timestampMs;
    setCurrentSessionEvents((current) => [fullEvent, ...current].slice(0, 300));
    setStatusMessage(
      `Recording ${sessionId}. Captured ${currentSessionEvents.length + 1} event${
        currentSessionEvents.length + 1 === 1 ? "" : "s"
      } in the current session.`,
    );
  };

  const startRecording = () => {
    resetSessionTracking();
    setIsRecording(true);
    setStatusMessage(
      `Recording started for ${sessionId} with target label "${selectedLabel}" inside ${currentApp.title}.`,
    );
  };

  const stopRecording = () => {
    if (!isRecording) {
      return;
    }

    const orderedEvents = [...currentSessionEvents].reverse();
    if (orderedEvents.length) {
      setSavedSessions((current) => [
        {
          session_id: sessionId,
          target_label: selectedLabel,
          app_id: currentAppId,
          page_id: currentPageId,
          recorded_at: new Date().toISOString(),
          event_count: orderedEvents.length,
          metadata: {
            app_id: currentAppId,
            page_id: currentPageId,
          },
          repo_saved_at: null,
          events: orderedEvents,
        },
        ...current,
      ]);
      setStatusMessage(
        `Saved ${orderedEvents.length} event${orderedEvents.length === 1 ? "" : "s"} for ${sessionId}.`,
      );
    } else {
      setStatusMessage(`Stopped recording ${sessionId}. No events were captured.`);
    }

    setIsRecording(false);
    setCurrentSessionEvents([]);
    setSessionId(buildSessionId(selectedLabel));
  };

  const clearAllSessions = () => {
    setSavedSessions([]);
    setCurrentSessionEvents([]);
    window.localStorage.removeItem(STORAGE_KEY);
    setStatusMessage("Cleared all locally stored sessions.");
  };

  const downloadCurrentSession = () => {
    const orderedEvents = [...currentSessionEvents].reverse();
    downloadJsonl(orderedEvents, `${sessionId}.jsonl`);
  };

  const downloadAllSessions = () => {
    downloadJsonl(allRecordedEvents, "captured_events.jsonl");
  };

  const appendEventsToRepoFile = async (events, filename) => {
    if (!events.length) {
      setStatusMessage("There is no captured data to save yet.");
      return false;
    }

    if (!supportsDirectRepoSave()) {
      downloadJsonl(events, filename);
      setStatusMessage(
        "This browser does not support direct repo appending, so the JSONL file was downloaded instead.",
      );
      return false;
    }

    setIsSavingToRepo(true);
    try {
      const directoryHandle = await window.showDirectoryPicker({
        id: "behavior-collector-data-raw",
        mode: "readwrite",
      });
      const fileHandle = await directoryHandle.getFileHandle(filename, { create: true });
      const existingFile = await fileHandle.getFile();
      const existingBody = (await existingFile.text()).trimEnd();
      const nextBody = buildJsonlBody(events);
      const writable = await fileHandle.createWritable();
      await writable.write(existingBody ? `${existingBody}\n${nextBody}\n` : `${nextBody}\n`);
      await writable.close();
      setStatusMessage(
        `Appended ${events.length} event${events.length === 1 ? "" : "s"} into ${filename}. Choose your repo's data/raw folder for direct training use.`,
      );
      return true;
    } catch (error) {
      if (error?.name === "AbortError") {
        setStatusMessage("Save to repo was cancelled.");
      } else {
        setStatusMessage(`Could not save into the repo: ${error.message}`);
      }
      return false;
    } finally {
      setIsSavingToRepo(false);
    }
  };

  const saveCurrentSessionToRepo = async () => {
    const orderedEvents = [...currentSessionEvents].reverse();
    await appendEventsToRepoFile(orderedEvents, `${sessionId}.jsonl`);
  };

  const saveAllSessionsToRepo = async () => {
    const didAppend = await appendEventsToRepoFile(
      unsavedRecordedEvents,
      "captured_events.jsonl",
    );
    if (!didAppend) {
      return;
    }

    const savedAt = new Date().toISOString();
    setSavedSessions((current) =>
      current.map((session) =>
        session.repo_saved_at ? session : { ...session, repo_saved_at: savedAt },
      ),
    );
  };

  const handleScroll = (event) => {
    if (!isRecording) {
      return;
    }

    const container = event.currentTarget;
    const now = Date.now();
    const currentTop = container.scrollTop;
    const deltaY = currentTop - lastScrollRef.current.top;
    const deltaTime = Math.max(1, now - lastScrollRef.current.timestamp);
    const velocity = Math.abs(deltaY / deltaTime) * 1000;
    const acceleration =
      ((velocity - lastScrollRef.current.velocity) / deltaTime) *
      1000 *
      (deltaY === 0 ? 1 : Math.sign(deltaY));

    lastScrollRef.current = {
      top: currentTop,
      timestamp: now,
      velocity,
    };

    recordEvent({
      event_type: "scroll",
      y: currentTop,
      delta_y: deltaY,
      velocity,
      acceleration,
      direction: deltaY === 0 ? 0 : Math.sign(deltaY),
    });
  };

  const handlePointerDown = (event) => {
    if (!isRecording) {
      return;
    }

    pointerDownRef.current = {
      timestamp: Date.now(),
      x: event.clientX,
      y: event.clientY,
      pressure: event.pressure ?? 0,
    };
  };

  const handlePointerUp = (event) => {
    if (!isRecording || !pointerDownRef.current) {
      return;
    }

    const duration = Date.now() - pointerDownRef.current.timestamp;
    recordEvent({
      event_type: "touch",
      x: event.clientX,
      y: event.clientY,
      pressure: event.pressure ?? pointerDownRef.current.pressure ?? 0,
      duration_ms: duration,
    });
    pointerDownRef.current = null;
  };

  const handleClick = (event) => {
    if (!isRecording) {
      return;
    }

    recordEvent({
      event_type: "click",
      x: event.clientX,
      y: event.clientY,
    });
  };

  const handleSelectionCapture = () => {
    if (!isRecording) {
      return;
    }

    const selection = window.getSelection();
    const text = selection?.toString()?.trim();
    if (!text) {
      return;
    }

    const wordCount = text.split(/\s+/).filter(Boolean).length;
    const focusNode = selection.focusNode?.parentElement;
    const rect = focusNode?.getBoundingClientRect();

    recordEvent({
      event_type: "selection",
      x: rect?.left ?? 0,
      y: rect?.top ?? 0,
      duration_ms: 1200,
      selection_word_count: wordCount,
    });
  };

  const switchApp = (appId) => {
    if (appId === currentAppId) {
      return;
    }

    const nextApp = APP_SIMULATORS.find((app) => app.id === appId) ?? APP_SIMULATORS[0];
    setCurrentAppId(nextApp.id);
    setCurrentPageId(nextApp.pages[0].id);
    if (surfaceRef.current) {
      surfaceRef.current.scrollTo({ top: 0, behavior: "smooth" });
    }
    lastScrollRef.current = { top: 0, timestamp: Date.now(), velocity: 0 };

    if (isRecording) {
      recordEvent({
        event_type: "navigation",
        x: 0,
        y: 0,
      });
    }
  };

  const switchPage = (pageId) => {
    if (pageId === currentPageId) {
      return;
    }

    setCurrentPageId(pageId);
    if (surfaceRef.current) {
      surfaceRef.current.scrollTo({ top: 0, behavior: "smooth" });
    }
    lastScrollRef.current = { top: 0, timestamp: Date.now(), velocity: 0 };

    if (isRecording) {
      recordEvent({
        event_type: "navigation",
        x: 0,
        y: 0,
      });
    }
  };

  const toggleTask = (taskLabel) => {
    setTaskChecks((current) => ({
      ...current,
      [taskLabel]: !current[taskLabel],
    }));
  };

  const renderDocumentPage = (page) => (
    <article
      className="reader panel"
      ref={surfaceRef}
      onScroll={handleScroll}
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onClick={handleClick}
      onMouseUp={handleSelectionCapture}
    >
      <div className="page-banner">
        <p className="eyebrow">{page.title}</p>
        <h2>{page.description}</h2>
      </div>
      {page.sections.map((section, index) => (
        <section key={section.id} className="article-section">
          <div className="section-meta">
            <span>{String(index + 1).padStart(2, "0")}</span>
            <p>{section.kicker}</p>
          </div>
          <div className="section-body">
            <h2>{section.title}</h2>
            {section.paragraphs.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
            <div className="detail-grid">
              <button className="detail-card">Open supporting note</button>
              <button className="detail-card">Compare this point</button>
              <button className="detail-card">Highlight for later</button>
            </div>
          </div>
        </section>
      ))}
    </article>
  );

  const renderTaskPage = (page) => (
    <section
      className="app-surface panel"
      ref={surfaceRef}
      onScroll={handleScroll}
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onClick={handleClick}
      onMouseUp={handleSelectionCapture}
    >
      <div className="page-banner">
        <p className="eyebrow">{page.title}</p>
        <h2>{page.description}</h2>
      </div>

      {page.variant === "tasks" ? (
        <div className="stack">
          {page.tasks.map((task) => (
            <label key={task} className="task-row app-card">
              <input
                type="checkbox"
                checked={Boolean(taskChecks[task])}
                onChange={() => toggleTask(task)}
              />
              <span>{task}</span>
            </label>
          ))}
        </div>
      ) : null}

      {page.variant === "board" ? (
        <div className="board-grid">
          {page.columns.map((column) => (
            <div key={column.title} className="app-card">
              <strong>{column.title}</strong>
              <div className="stack">
                {column.items.map((item) => (
                  <button key={item} className="detail-card">
                    {item}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : null}

      {page.variant === "calendar" ? (
        <div className="stack">
          {page.slots.map((slot) => (
            <div key={slot} className="app-card">
              <div className="metric-row">
                <strong>{slot}</strong>
                <button className="detail-card">Open</button>
              </div>
            </div>
          ))}
        </div>
      ) : null}

      {page.variant === "task_analytics" ? (
        <div className="metric-cards">
          {page.metrics.map((metric) => (
            <div key={metric.label} className="app-card">
              <p className="card-kicker">{metric.label}</p>
              <strong className="big-value">{metric.value}</strong>
              <div className="detail-grid">
                <button className="detail-card">Inspect</button>
                <button className="detail-card">Compare</button>
              </div>
            </div>
          ))}
        </div>
      ) : null}
    </section>
  );

  const renderCurrentAppSurface = () => {
    if (currentApp.id === "document_reader") {
      return renderDocumentPage(currentPage);
    }
    return renderTaskPage(currentPage);
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Behavior Collector</p>
          <h1>Generate labeled training data across multiple simulated apps</h1>
          <p className="hero-copy">
            Pick a behavior label, switch between app types and pages, and save the captured raw
            events into your repo without changing the training schema.
          </p>
        </div>
        <div className="status-pill ok">Frontend-only capture</div>
      </header>

      <main className="layout">
        <aside className="panel controls">
          <h2>Session Controls</h2>
          <label className="field">
            <span>Target label</span>
            <select
              value={selectedLabel}
              onChange={(event) => setSelectedLabel(event.target.value)}
              disabled={isRecording}
            >
              {COLLECTOR_LABELS.map((label) => (
                <option key={label} value={label}>
                  {label}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Session id</span>
            <input
              value={sessionId}
              onChange={(event) => setSessionId(event.target.value)}
              disabled={isRecording}
            />
          </label>

          <div className="button-row">
            <button className="primary" onClick={startRecording} disabled={isRecording}>
              Start recording
            </button>
            <button className="secondary" onClick={stopRecording} disabled={!isRecording}>
              Stop recording
            </button>
          </div>

          <div className="button-row">
            <button
              className="secondary"
              onClick={saveCurrentSessionToRepo}
              disabled={!currentSessionEvents.length}
            >
              Append current to repo
            </button>
            <button
              className="secondary"
              onClick={saveAllSessionsToRepo}
              disabled={!unsavedRecordedEvents.length || isSavingToRepo}
            >
              Append all to repo
            </button>
          </div>

          <div className="button-row">
            <button
              className="secondary"
              onClick={downloadCurrentSession}
              disabled={!currentSessionEvents.length}
            >
              Download current
            </button>
            <button
              className="secondary"
              onClick={downloadAllSessions}
              disabled={!allRecordedEvents.length}
            >
              Download all
            </button>
          </div>

          <div className="button-row">
            <button
              className="secondary"
              onClick={clearAllSessions}
              disabled={!savedSessions.length && !currentSessionEvents.length}
            >
              Clear stored data
            </button>
          </div>

          <p className="status-text">{statusMessage}</p>

          <section className="summary-card">
            <h3>Capture Summary</h3>
            <div className="metric-row">
              <span>Current app</span>
              <strong>{currentApp.title}</strong>
            </div>
            <div className="metric-row">
              <span>Current page</span>
              <strong>{currentPage.title}</strong>
            </div>
            <div className="metric-row">
              <span>Current session events</span>
              <strong>{currentSessionEvents.length}</strong>
            </div>
            <div className="metric-row">
              <span>Total stored events</span>
              <strong>{totalEventCount}</strong>
            </div>
            <div className="metric-row">
              <span>Pending repo append</span>
              <strong>{unsavedRecordedEvents.length}</strong>
            </div>
            <p className="muted">
              App and page metadata is stored only in local session state for future use. The
              exported JSONL keeps the same raw-event schema as before.
            </p>
          </section>
        </aside>

        <section className="reader-panel">
          <nav className="app-nav panel">
            <h2>Simulated Apps</h2>
            <div className="page-grid">
              {APP_SIMULATORS.map((app) => (
                <button
                  key={app.id}
                  className={`page-card ${app.id === currentAppId ? "active" : ""}`}
                  onClick={() => switchApp(app.id)}
                >
                  <strong>{app.title}</strong>
                  <span>{app.description}</span>
                </button>
              ))}
            </div>
          </nav>

          <nav className="page-nav panel">
            <h2>{currentApp.title} Pages</h2>
            <div className="compact-grid">
              {currentApp.pages.map((page) => (
                <button
                  key={page.id}
                  className={`compact-card ${page.id === currentPageId ? "active" : ""}`}
                  onClick={() => switchPage(page.id)}
                >
                  <strong>{page.title}</strong>
                </button>
              ))}
            </div>
          </nav>

          {renderCurrentAppSurface()}
        </section>
      </main>
    </div>
  );
}

export default App;
