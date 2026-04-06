# Behavior Collector App

This is a separate React web app used to collect labeled interaction sessions
for model training across a simulated document reader and task manager.

## What It Does

- choose a target behavior label before recording
- switch between a long-form document reader and a task manager
- navigate across multiple pages inside each simulated app
- capture raw interaction events without changing the existing training-event format
- keep the captured events locally in browser storage
- save the events directly into the repo as JSONL if the browser supports the File System Access API
- download the events as JSONL as a fallback
- generate navigation events by moving across apps and pages

## Run The App

In this folder install and run the React app:

```bash
npm install
npm run dev
```

Use the app like this:

1. Choose a target behavior label.
2. Start recording.
3. Move between the simulated apps and their pages, then interact with the current UI.
4. Stop recording.
5. Click `Append all to repo` and choose the repo's `data/raw` folder.
6. If direct saving is unavailable, use the download fallback instead.

The captured data is stored in browser local storage until you save or export it.

## Training Flow After Collection

If you used `Append all to repo`, pick:

- `/Users/dhanesh/Desktop/p/user-behavior-tracker/data/raw/`

The app writes:

- `captured_events.jsonl` for all saved sessions
- or `<session_id>.jsonl` for the current session

## Important Notes

- `Append all to repo` appends only sessions that have not already been pushed
  into the repo from this browser state, so repeated clicks do not keep
  duplicating the same saved sessions.
- `Append current to repo` appends the in-progress session events into its
  session-specific JSONL file.
- The exported event JSONL keeps the same raw event schema used by the current
  training pipeline.
- App and page metadata are kept only in the browser session state for future
  use and are not added to the exported training events yet.

Then go back to the repo root and run:

```bash
python src/preprocess.py
python src/train.py
python src/evaluate.py
```

Because preprocessing reads every JSONL file in `data/raw/`, the exported
sessions are included automatically once they are saved there.
