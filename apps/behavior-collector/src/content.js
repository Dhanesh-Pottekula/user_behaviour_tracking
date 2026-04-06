export const COLLECTOR_LABELS = [
  "skimming",
  "hunting",
  "normal",
  "ignore",
  "frustrated",
  "engaged",
  "confused",
  "comparing",
  "deep_reading",
];

const createStory = (id, title, kicker, paragraphs) => ({
  id,
  title,
  kicker,
  paragraphs,
});

const volumeOneStories = [
  createStory("glass-harbor", "Story 1: The Glass Harbor", "Coastal fiction", [
    "By the time the morning ferries reached the breakwater, the harbor looked as if it had been assembled from mirrors. Nets shimmered on the decks, gulls cut pale loops above the water, and the oldest fishers leaned against painted rails as though they were waiting for news rather than weather.",
    "Mira kept her ledger open on a crate beside the ice bins because she never trusted memory on market days. She counted blue crabs, wrote down fuel prices, crossed out a supplier's promise, and watched the new shipping clerk run from boat to boat with the nervous urgency of someone trying to outrun his first mistake.",
    "Around noon a crate stamped with the wrong pier number arrived at the harbor office. It contained not shellfish or rope fittings but a bundle of handwritten tide charts and three letters addressed to people who had been dead for years. Mira stood with the packet in both hands and felt the harbor change from a workplace into a puzzle.",
    "That evening, after most of the boats had gone silent, she followed the oldest tide line down the seawall and found a locked steel cabinet bolted behind a stack of storm shutters. The key was not in the packet, but the dates in the letters matched the etchings on the cabinet door. For the first time in years, the harbor looked less like a business she managed and more like a story still trying to finish itself.",
  ]),
  createStory("night-train", "Story 2: The Night Train to Saffron Junction", "Railway mystery", [
    "The train left the capital twenty minutes late, which was enough to shift every conversation aboard it. Missed connections turned to long apologies, station agents traded impatient notes over radios, and a violinist in carriage C decided that a delayed audience was an audience worth testing with more ambitious music.",
    "Arun boarded with a single canvas bag and a borrowed map that had too many penciled corrections to be official. He had been told to meet a surveyor in Saffron Junction, but the only thing he knew for certain was the compartment number written on the back of his ticket and the warning to trust no timetable printed after March.",
    "Near midnight the conductor announced a routing change that sent murmurs through the corridors. Some passengers pretended not to care. Others leaned into the windows, trying to measure their location by the silhouettes of signal towers. Arun noticed that the woman across from him folded the same newspaper headline three times without reading beyond the first paragraph.",
    "When the train finally stopped between stations, every carriage held its breath. A man in a postal jacket crossed the gravel in the rain and delivered a sealed envelope directly to the conductor. Five minutes later the lights in two carriages went dark, and the violinist in carriage C kept playing as though music were the only way to keep the train from dissolving into the fields around it.",
  ]),
  createStory("orchard-ledger", "Story 3: The Orchard Ledger", "Family archive", [
    "The orchard sat on a hillside where the wind arrived before the sun. Every row of pear trees had been mapped decades earlier by hand, and the family still used the old numbering system even though no one remembered why the southern slope began with row fourteen instead of row one.",
    "Leela came back in late autumn to catalog the farm books before the land transfer closed. She expected invoices, rainfall notes, harvest yields, and the minor arithmetic of a property passing from one generation to another. Instead she found ledger margins filled with observations about neighbors' departures, local elections, and the exact evenings when frost arrived earlier than predicted.",
    "The deeper she read, the clearer it became that the ledgers were not side notes to the orchard but the orchard's real history. Trees had been replanted after arguments, fields had been divided after weddings, and the smallest yield swings matched moments of grief or stubbornness more closely than they matched weather.",
    "On the final afternoon she discovered a folded inventory sheet hidden between two pest-control reports. It listed tools no one in the family owned, debts no one had admitted, and a final line that simply read, 'North gate key returned with the winter geese.' Leela looked toward the ridge road where the abandoned gate still leaned crookedly and realized the orchard had been keeping secrets longer than it had been growing fruit.",
  ]),
  createStory("station-lantern", "Story 4: The Station Lantern", "Small-town suspense", [
    "Every evening at six, the stationmaster lit the platform lantern even though no train had stopped in Belden for fourteen years. Children treated the ritual like part of the weather. Travelers treated it like folklore. Only Rafi, who had recently returned to catalog the village archives, treated it like evidence.",
    "The lantern records were surprisingly precise. Fuel deliveries, wick changes, brass repairs, and weather notes had been logged as faithfully as if the line were still active. Yet on two nights every autumn the ink changed color and the remarks stopped mentioning wind speed. Instead they listed passenger counts for trains that officially no longer existed.",
    "Rafi waited through the first of those dates with a notebook and a thermos. Nothing came. No whistle, no lights, no footsteps. Yet the stationmaster still raised a hand toward the curve of track at 6:14 as if acknowledging someone stepping down from a carriage. In the ledger for that same minute, the phrase 'two alight, one remains' appeared without any scratch or hesitation.",
    "On the second date, fog moved across the rails so evenly it resembled cloth being drawn over a table. A single compartment window glowed inside it, then another. By the time Rafi ran to the edge of the platform, the fog had already begun to thin. In the wet gravel he found three suitcase marks and one heel print leading toward the orchard road, where no one in Belden claimed to have gone that night.",
  ]),
  createStory("seventh-bell", "Story 5: The Seventh Bell", "Monastery tale", [
    "The monastery bells were supposed to ring six times at dawn, once for each terrace cut into the mountain. Novices learned the pattern before they learned the paths. So when a seventh bell sounded one winter morning, everyone assumed wind had struck the bronze in some rare and convenient way.",
    "Only Sumi noticed that the seventh note carried no echo. It sounded close, flat, and deliberate, like a bell rung inside a room too small for reverence. She spent the day tracing the monastery's older plans and found that the eastern dormitory had once connected to a library wing removed from every modern map.",
    "The elders dismissed her questions until she showed them a repair log dated eighty years earlier. A carpenter had noted fresh rope grooves on a beam where no bell was supposed to hang. He had also sketched a doorway hidden behind a cupboard of winter robes. The note ended with a warning to 'leave the interior bell unanswered after snowfall.'",
    "That night Sumi slid the cupboard aside and entered a stairwell lined with soot-dark plaster. At the bottom stood a chapel no one had mentioned in lessons, its rafters holding a bronze bell smaller than a cooking pot. Tied to its clapper was a strip of red cloth embroidered with names, each one belonging to someone who had vanished from the monastery census during harsh winters and had somehow continued to ring for remembrance after everyone forgot the room existed.",
  ]),
  createStory("salt-maps", "Story 6: Salt Maps", "Merchant voyage", [
    "Captain Ilya bought the maps at an inland auction where nothing smelled remotely nautical. They were rolled inside a carpenter's tube, dusted with chalk, and labeled in a hand too neat for a sailor. At first glance they showed ordinary coastlines. At second glance they contradicted every harbor depth sounding recorded during the last decade.",
    "His first mate laughed until the ship reached the first disputed inlet and found water where charts said stone should be. The new passage was narrow, quiet, and lined with white cliffs that looked like stacked salt blocks. Halfway through, the compass began drifting toward the cliff walls as though the coastline itself had learned how to pull metal into obedience.",
    "The crew wanted to turn back, but the map included side notes naming safe currents, anchor points, and even a freshwater spring hidden behind a collapsed boathouse. Whoever drew it had traveled this secret channel more than once. At the final bend they found a wharf built from cedar too old to float yet somehow still standing above deep clear water.",
    "Nailed to the wharf post was a customs placard bearing the seal of a kingdom dissolved before Ilya's grandfather was born. Under the seal someone had etched a newer message with a knife point: 'Routes forgotten by governments remain visible to ships with the patience to arrive late.' Ilya rolled the maps carefully back into their tube and realized he had not purchased directions so much as inherited a dispute with history.",
  ]),
  createStory("paper-garden", "Story 7: The Paper Garden", "Literary fantasy", [
    "At the edge of the botanical conservatory stood a greenhouse reserved for educational exhibits and plants too delicate for the public halls. Eva expected seedlings and instructional charts when she accepted the summer archivist post. Instead she found waist-high beds filled with paper leaves pinned to wire stems, each one written on in different handwriting.",
    "The gardeners treated the paper beds with complete seriousness. They misted them, turned them toward the light, and replaced brittle stems with thin lacquered rods. When Eva asked what species they were preserving, the head gardener told her they were unfinished descriptions from extinct field journals. If they were not kept in sequence, he said, the missing plants disappeared twice.",
    "Each leaf carried a sensory note rather than a name: bitter after rain, silver along the underside, opens only near old stone. As weeks passed, Eva realized the notes formed clusters. Four leaves described one fern seen near a ruined observatory. Seven described a vine that had strangled church bells in abandoned river towns. None of the plants existed in the official catalog.",
    "On her final day she found a blank leaf newly pinned to the center bed. Overnight it had absorbed a faint line of ink: broad petals, scent of warm dust, found where paper is watered. The gardeners pretended not to notice her reading it, but one of them silently placed a watering can in her hands. By evening, a pale folded flower had opened between the pages of her notebook where she had pressed the leaf for safekeeping.",
  ]),
  createStory("granite-school", "Story 8: Lessons at Granite School", "Institutional mystery", [
    "Granite School sat above the quarry on a rise of land everyone called temporary even though the building had survived earthquakes, three changes in curriculum, and the slow abandonment of the town below it. The classrooms were drafty, the chemistry sinks leaked, and every graduating class left behind at least one rumor about a locked room somewhere under the assembly hall.",
    "When new headteacher Daman reviewed the maintenance budget, he found a recurring line item for slate dust containment in a wing the school no longer had. No contractor could explain it. The oldest custodian only shrugged and said the dust had to be paid attention to or it would begin writing again.",
    "That sentence bothered Daman enough to pry up an access panel behind the stage curtains. A narrow set of stairs led to an old geology lab with wall maps painted directly onto stone. The benches were covered in gray powder, but the chalkboards were clean except for one equation repeated from left to right in increasingly hurried handwriting.",
    "It was not an equation at all. It was a timetable disguised as one, charting after-school meetings that had taken place during the strike winter thirty years earlier. The final line ended with room numbers for students who had vanished from the enrollment records. When Daman compared the names to the alumni honor roll in the main hall, he discovered that the missing students had not been erased. They had been promoted into memorial plaques without anyone ever recording the day they stopped attending class.",
  ]),
  createStory("weather-cabinet", "Story 9: The Weather Cabinet", "Scientific curiosity", [
    "Professor Nira inherited the observatory's weather cabinet along with a retired telescope and six unpaid invoices. The cabinet was oak, scarred by seawater, and divided into narrow drawers labeled with terms no meteorologist used anymore: candle rain, slate light, harbor frost, hinge wind.",
    "Inside each drawer she found not instruments but folded strips of tissue paper marked with atmospheric notes. Some were practical, measuring pressure changes or unusual gusts. Others read more like prophecies: gulls circle inland two days before hinge wind; lamps burn lower under candle rain even in closed rooms.",
    "Skeptical but curious, Nira cross-checked the notes against the observatory's digital archive. Too many matched. Events written in idiosyncratic, almost poetic terms aligned neatly with storms, coastal inversions, and microbursts documented a century later with modern precision. Whoever kept the cabinet had invented a parallel language for weather and somehow been right more often than the official station.",
    "The final drawer was locked. She opened it with a brass key taped beneath the cabinet top and found a blank stack of tissues beside a note: 'These terms are only names until someone is willing to continue them.' Outside, the afternoon sky darkened with the peculiar yellow-gray light the old papers called lantern rain. Without fully deciding to, Nira took up a pencil and began a new label before the storm arrived.",
  ]),
  createStory("island-choir", "Story 10: The Island Choir", "Sea-bound finale", [
    "The island's choir had not performed for visitors in generations, but every equinox the ferryman still crossed at dusk with an empty second boat tied behind his own. City officials called it ceremonial tourism. The ferryman called it attendance.",
    "Journalist Tanu followed him across the channel expecting staged folklore. Instead she found a chapel open to the wind, its pews empty and its music stands set with sheets too watermarked to read in full. The choir members who did arrive were old, quiet, and more interested in lighting the side lanterns than speaking to outsiders.",
    "When the singing began, it seemed thin at first, almost conversational. Then a second harmony entered from somewhere beyond the open west wall where nothing stood but cliff grass and surf. No one inside the chapel reacted with surprise. The ferryman simply shifted one boat rope farther up the post, making space for another vessel that never became visible in the cove.",
    "After the final note, the conductor handed Tanu a program dated fifty-two years earlier. Every listed singer from the lower harmony had died in the winter storm that severed the old ferry route. 'We stopped announcing the absences,' the conductor said, folding the damp paper back into her hand. 'It sounded crueler than letting the music remember for us.'",
  ]),
];

const volumeTwoStories = [
  createStory("ash-library", "Story 11: The Ash Library", "Urban fantasy", [
    "The city archive had burned forty years before Nalin was born, yet people still gave directions using its old address. Turn left at the ash library, they said, even though the building no longer stood and the plaza now held a tram stop, a coffee kiosk, and a fountain that never worked in summer.",
    "Nalin restored damaged books for the municipal museum, which meant that strangers often arrived carrying boxes rescued from floods, attics, and inheritances. One rainy Tuesday a retired magistrate dropped off a set of warped volumes wrapped in sailcloth. Their pages were blackened at the edges, but the damage did not match heat. It looked more like the books had been singed from inside.",
    "As he cleaned the first binding, a list of names appeared in silver script beneath the soot. Every name belonged to someone who had testified during the archive fire inquiry, and every date had been crossed out except one. That uncrossed date was next week.",
    "Nalin spent three evenings tracing ownership stamps, delivery markings, and shelf codes that no longer existed. The pattern led him to a service tunnel under the tram plaza, where the air smelled faintly of paper dust. At the far wall he found a steel grate painted with the museum's old emblem. Behind it, shelves ran into the dark, and on those shelves sat hundreds of books the city had insisted were lost forever.",
  ]),
  createStory("desert-signal", "Story 12: Desert Signal", "Expedition journal", [
    "At Camp Meridian, every radio message was copied twice: once for logistics and once for morale. The first list kept the convoy moving. The second kept people from imagining the dunes were swallowing the map one coordinate at a time.",
    "Ishaan led the survey team because he was patient enough to trust instruments without worshipping them. He believed every machine eventually confessed its bias if you listened long enough. The problem with the desert station was that the instruments had started agreeing too perfectly, which meant either the calibration was miraculous or the entire ridge was telling the same lie.",
    "The signal appeared each dusk, seven notes rising and falling in a pattern too orderly to be wind and too irregular to be military traffic. The camp medic heard grief in it. The mechanic heard a generator fault. Ishaan heard spacing, as though the signal were marking distances between things no one could yet see.",
    "On the fifth night he drove beyond the marked route with only one antenna mast strapped to the truck bed. The dunes opened into a basin of dark stone, and at the center stood six weather towers arranged in a ring. Their serial numbers belonged to a research program canceled fifteen years earlier. The seventh tower was missing, but its shadow remained on the ground, narrow and sharp, as if the desert still expected it to return before dawn.",
  ]),
  createStory("narrow-house", "Story 13: The Narrow House on Vesper Lane", "Quiet suspense", [
    "No one bought the narrow house for its beauty. They bought it because it sat between two large homes on a street where any extra square meter doubled in value every decade. Estate agents called it efficient. Contractors called it inconvenient. Neighbors called it temporary, though it had been there longer than any of them.",
    "Rhea rented the top floor because she liked inconvenient spaces. They forced people to reveal their habits. In the narrow house she learned how sound traveled through pipe chases, which boards answered to humidity, and which wall shook when the woman downstairs opened the pantry too sharply.",
    "Three weeks after moving in, she began receiving mail with no stamps and no sender. Each envelope contained a single room measurement written in blue ink. The numbers were precise down to the centimeter, but none matched the official survey filed with the lease. The dimensions described a house slightly wider than the one she inhabited.",
    "Rhea started measuring at night, pressing the tape against baseboards and window frames while the stairwell cooled around her. By the fourth envelope she was convinced there was a missing shaft running through the center of the building. By the sixth, she found the panel under the attic ladder. Behind it was a cavity lined with plaster and old wallpaper, wide enough for one person to stand in silence while the rest of the house went on believing it was alone.",
  ]),
  createStory("cedar-market", "Story 14: The Cedar Market", "Trade quarter drama", [
    "The cedar market opened before sunrise because spice merchants trusted cool air more than customers. By seven in the morning the square smelled of cardamom, lamp oil, damp rope, and the first bread from the hill ovens. Vendors shouted inventories across the stalls with the rhythm of people keeping the district stitched together by habit.",
    "When accountant Farid came to audit the market guild, he expected underreported rents and overreported repairs. Instead he found entire stall rows paying taxes to businesses that no longer existed. The signatures changed each quarter, but the hand pressure in the ledger margins stayed the same, as if one careful clerk had spent years pretending to be a committee.",
    "He followed the trail through delivery tags, seal impressions, and warehouse keys until it pointed him toward a shuttered cedar workshop on the north lane. Inside stood shelves full of unused stall placards painted with family names erased from the neighborhood after the flood decade. Someone had kept their licenses alive in paperwork even after the streets forgot their doors.",
    "The oldest tea seller in the market watched Farid lock the workshop again and said he should not report everything at once. 'If you clear the names too quickly, the square will feel smaller than it really is,' she told him. Farid looked across the waking market and realized the fraud he had uncovered was also, in a stubborn and unlawful way, a memorial system that still made room for the missing at opening bell.",
  ]),
  createStory("hinterland-post", "Story 15: Hinterland Post", "Postal mystery", [
    "The postal route beyond Mile Eight existed mostly because no one had formally canceled it. The villages were sparse, the roads flooded each spring, and every year's budget meeting ended with someone wondering aloud whether the hinterland had become too small to justify regular delivery.",
    "Courier Jana took the route anyway because some addresses continued replying to official letters faster than the city departments that questioned her fuel requests. She knew which farm dogs barked at uniforms, which bridges could bear a van after rain, and which hilltop houses always smelled faintly of solder and medicinal herbs.",
    "One week she began receiving sacks sorted in perfect route order but postmarked from no central depot. The sacks contained ordinary mail, yet tucked between them were sealed envelopes addressed to properties demolished years ago. Each envelope carried identical handwriting and a return symbol shaped like a split branch.",
    "Following the phantom route markers, Jana found an abandoned sorting shed hidden behind a quarry spoil ridge. Inside, a retired cancellation machine still worked, powered by a bicycle flywheel and a battery bank patched together from farm equipment. On the wall hung a pinned map connecting every demolished home to one still standing household nearby. Someone had rebuilt the postal network by hand so that no family's last known address would ever entirely vanish from the country's memory.",
  ]),
  createStory("velvet-obelisk", "Story 16: The Velvet Obelisk", "Museum noir", [
    "The obelisk arrived wrapped in theater velvet, which should have warned everyone at the museum that provenance was going to be a performance rather than a fact. It was too small for an imperial monument, too elegant for a grave marker, and inscribed with symbols that seemed to change depth depending on how the gallery lights were angled.",
    "Curator Dev promised the board a conservative cataloging process. Then the first translation draft suggested the stone was not commemorative at all but directional. The symbols matched warehouse marks used by caravan guilds, and the four polished faces aligned exactly with roads that no longer entered the modern city.",
    "Each time the obelisk was rotated for photography, visitors began asking guards for directions to places the museum had never exhibited: the seventh caravan court, the lower spice basin, the violet gate. Those names appeared nowhere on current maps. They did, however, appear in customs ledgers from the era before the river diversion turned the old trade district into reclaimed land.",
    "Dev tested the theory after closing. He stood the obelisk on a transport trolley, turned one face toward the museum's north exit, and followed a line of archived road names through three parking lots and a tram viaduct to a fenced-off excavation pit. At the bottom of the pit, beneath utility markings and puddled rain, the stone paving of the missing caravan court waited under exactly enough soil to make forgetting it seem accidental.",
  ]),
  createStory("quiet-reservoir", "Story 17: The Quiet Reservoir", "Environmental mystery", [
    "The reservoir had been called quiet long before the engineers arrived, though no one agreed on whether the name referred to the water or the valley under it. Fishermen said the winds dropped there without explanation. Surveyors said the acoustics swallowed distance. The first resettlement notices called it Zone C and hoped the older name would fade.",
    "Hydrologist Meher inherited the monitoring station after a software migration corrupted two years of inflow data. As she rebuilt the records from paper binders and backup drives, she noticed that the missing months aligned with nights when the spillway gates had been opened without any corresponding storm.",
    "The official explanation blamed sensor faults. Yet every manual gauge in the archive room showed the same midnight drawdowns. The reservoir level fell in small precise steps, then recovered by dawn as though some hidden channel were borrowing water for a few hours at a time and returning it before inspection rounds began.",
    "With the help of an elderly valve technician, Meher followed an abandoned service tunnel to a bricked chamber below the east embankment. Behind the new wall ran an older conduit lined with carved stone, not concrete. It carried a trickle of water toward the drowned valley church whose spire still surfaced in dry years. The engineers had not built a leak. They had preserved a submerged river rite and disguised it as bad recordkeeping.",
  ]),
  createStory("marble-kites", "Story 18: Marble Kites", "Festival chronicle", [
    "Every spring the hill city held a kite festival on the marble terraces above the courthouse, and every spring at least one elder insisted the tradition began as a legal protest, not a celebration. Children ignored that version because it involved tax petitions. Tourists ignored it because the bright paper skies were easier to photograph than the city's archive room.",
    "Research assistant Pavi only became interested when she found court transcripts mentioning signal strings, coded tails, and witness accounts that described entire verdicts being announced through kite patterns after magistrates were ordered not to publish them. The terrace had once been less of a park and more of an airborne bulletin board for unpopular truths.",
    "Pavi compared the old testimony to surviving kite designs in the museum collection and found recurring shapes embedded inside the festival's decorative motifs: a hooked tail for acquittal, paired red circles for unpaid wages, a mirrored chevron for land seizure appeals. The citizens had kept flying the code long after most of them forgot how to read it.",
    "During the modern festival's final round, a gust tore one champion kite against the courthouse balustrade, exposing a layered tail construction that only made sense if it still carried message grammar. Pavi looked around at the families cheering in the sun and understood that the city had not lost its protest language. It had disguised it as tradition so thoroughly that it could survive even official nostalgia.",
  ]),
  createStory("brass-weather", "Story 19: Brass Weather", "Clockmaker's tale", [
    "The clockmaker's quarter was loud by habit and quiet by reputation. Tourists came for the hourly tower melody, but locals knew the better sound was the workshop hour before opening, when dozens of tiny springs were being tested behind narrow windows and the whole lane trembled with private industry.",
    "Apprentice Hema was cataloging surplus parts when she discovered a crate of brass discs punched with cloud symbols instead of numbers. Her master claimed they were decorative rejects from a civic weather clock never completed. The city archivist, however, produced procurement orders showing the clock had been built, installed, and maintained for nearly eleven years before vanishing from all photographs.",
    "Further digging revealed maintenance notes filed under the astronomy bureau rather than the clock guild. The mechanism had not predicted weather; it had synchronized rooftop observers across the city by translating wind shifts and pressure changes into visible brass positions. Its disappearance coincided with the end of a period when smog inversions trapped factory fumes over the river wards.",
    "Hema finally found the weather clock dismantled inside a bell tower loft, every disc wrapped in cloth and labeled by district. Reassembling even a portion of it would expose how early officials had known about the poison air and how carefully they had hidden the warning system once it became politically expensive. She ran her thumb over the cloud symbols and realized the crate contained not failed ornament but archived accountability.",
  ]),
  createStory("lantern-quarry", "Story 20: Lantern Quarry", "Cliffside ending", [
    "The quarry had flooded decades ago, leaving terraces of black water and white stone where lantern festivals were now held each autumn. Visitors floated paper lights on the upper pools and called it beautiful. Workers who had once cut stone there called it unfinished.",
    "Documentarian Omi came to record oral histories and found that every interview circled the same missing topic. People remembered wages, injuries, songs, lunch sheds, and storm seasons, but no one wanted to describe the final week before the pumps were shut off. A union flyer from that week listed a meeting at Shaft Four that, according to the town chronicle, had never happened.",
    "At festival dusk he followed the old haul road with a retired driller named Sena, who carried a lantern too heavy for ceremony. They descended to a dry maintenance gallery behind the lowest pool and found chalk tallies covering the wall: names, tool counts, and a running estimate of hours spent sealing a lateral tunnel no map acknowledged.",
    "Sena admitted the workers had discovered a second quarry inside the first, an older cut full of carved pillars and ritual basins. Flooding the public site had concealed the strike accident and the archaeological scandal at once. When the festival lanterns drifted overhead that night, their reflections shivered across the hidden stone ceiling, and Omi understood why the town had chosen remembrance by water rather than by speech.",
  ]),
];

const volumeThreeStories = [
  createStory("winter-clinic", "Story 21: Winter Clinic", "Mountain town drama", [
    "The clinic served six villages, three logging camps, and one observatory that only became visible after heavy snow. In winter the road disappeared twice a week, and appointments were scheduled according to whichever rumors about avalanches sounded least reliable.",
    "Dr. Samira kept patient charts in color-coded folders because the heating system failed so often that labels peeled off by February. One stormy evening a courier arrived with a stack of records from the shuttered lower-valley hospital. The files were supposed to be routine transfers, but several included treatment notes signed by a physician who had retired before those patients were born.",
    "At first she assumed the records had been copied incorrectly. Then she noticed the lab timestamps. Tests marked as completed during blizzard closures matched nights when every road monitor showed total shutdown. The only functioning route would have been the old supply lift on the north ridge, a system dismantled five winters ago after a cable snapped.",
    "Samira climbed to the ridge station before sunrise, following maintenance flags buried under fresh snow. The lift house stood locked and half drifted in, yet inside she found recent generator fuel, sterilized trays, and a wall map pricked with six red pins. Each pin matched a patient from the transferred files. Whoever had been treating them had built a second clinic in the mountains and had been careful enough to leave no name anywhere except the forged signatures in the charts.",
  ]),
  createStory("river-math", "Story 22: River of Small Numbers", "Historical puzzle", [
    "In the province archives there was a ledger no one requested because no one could read it all the way through. The script changed every dozen pages, the columns shifted without warning, and at odd intervals the clerk who wrote it abandoned language altogether and recorded entries as strings of tiny triangles.",
    "Tomas volunteered to translate it because he had spent five years cataloging irrigation records and had developed a strange affection for impossible bookkeeping. The first hundred pages concerned ferry tolls and bridge repairs. The next hundred appeared to track grain purchases. After that the ledger narrowed into a single recurring pattern: three names, seven villages, and the same small subtraction repeated at monthly intervals.",
    "He plotted the numbers on tracing paper and noticed they matched river depth changes along a tributary that no longer existed on modern maps. The subtraction was not tax, weight, or debt. It was water disappearing from one route and appearing in another, rewritten as accountancy to keep someone from asking why the canal inspectors never found it.",
    "The final pages led him outside the archive to an abandoned customs house beside a dried inlet. Behind a collapsed wall he uncovered a brass gauge still marked with the same triangular symbols. The province had not lost a river by accident; someone had hidden it inside the books and waited for the paperwork to outlive the witnesses.",
  ]),
  createStory("museum-midnight", "Story 23: Midnight at the Museum of Tools", "Character study", [
    "The Museum of Tools closed at six, but its director preferred the building after midnight, when every display label stopped sounding educational and started sounding like a confession. Objects built to fix roofs, lift gates, shape timber, and mend watches seemed less interested in history than in all the work they had not finished.",
    "Helena had inherited the directorship from a curator who documented everything except his reasons. In his office she found immaculate acquisition records, perfect exhibition budgets, and a locked drawer full of visitor comment cards sorted by handwriting instead of date. Each stack belonged to one anonymous visitor who had spent years returning to the museum without ever signing a name.",
    "The cards described tiny errors in the displays: a brace displayed with the wrong screw, a lathe part paired with a later model, a carpenter's compass positioned at the wrong angle. No casual visitor would have noticed. Whoever wrote them knew the tools not as artifacts but as working instruments.",
    "On the last Friday of the month Helena left the side door unlatched and waited in the restoration room with the lights off. Just after eleven a figure moved through the woodworking gallery, stopping only at the mislabeled pieces. He did not steal anything. He corrected the placements with the care of someone setting a table for absent family. When Helena switched on the lamp, he looked more relieved than startled and said, before she could ask his name, 'I only came back because they were still being displayed as if they had never been used.'",
  ]),
  createStory("last-observatory", "Story 24: The Last Observatory", "Slow-burn ending", [
    "The observatory on Kestrel Peak had been downgraded from research station to historical site when the new orbital array came online. Funding vanished, graduate students stopped applying, and the remaining astronomers learned to speak about budgets with the same tired patience they used for clouds.",
    "Anika arrived to inventory the remaining instruments before the closure ceremony. She expected a melancholy assignment: label the lenses, photograph the brass mounts, note which shutters jammed in damp air. Instead she found the dome floor marked with chalk circles and the logbooks from the last three months missing from the archive cabinet.",
    "The caretaker insisted no research had been conducted there since the downgrade. Yet the motors were warm, a set of star charts had been annotated in three different inks, and someone had recalibrated the oldest telescope to track an object too dim for public demonstration. Every night at 2:17 the dome opened for exactly fourteen minutes and then closed again.",
    "On the final night before the ceremony, Anika stayed through the coldest part of the mountain dark and watched the old instrument rise. Through the eyepiece she saw not a comet or a satellite but a faint procession of mirrored lights moving in formation beyond the cataloged field. In the missing logbook's place, the caretaker had left a note under the drawer lining: 'If they ask whether the observatory is still useful, tell them it has only just begun to be early enough.'",
  ]),
  createStory("amber-hospital", "Story 25: The Amber Hospital", "Civic gothic", [
    "The abandoned children's hospital at Amber Square was considered architecturally important and emotionally unusable, which meant every city council proposed preserving it and every budget committee quietly delayed the plan. Ivy threaded through shattered sunrooms, and the upper wards glowed gold at dusk as if the building still remembered visiting hours.",
    "Architect Noor received the survey commission because she specialized in structures people talked around rather than about. The plans were orderly until the pediatric wing, where corridors shifted by half-meters from floor to floor and stair labels skipped numbers the way anxious people skip explanations.",
    "In the records basement she found maintenance requests for a mobile classroom that appeared in payroll documents long after the hospital closed. The teachers assigned to it had no personnel files, yet the supply invoices listed fresh chalk, brass locks, and sugar biscuits delivered every winter to a room no floor plan admitted existed.",
    "Noor eventually reached that hidden classroom through a linen lift shaft bricked over at ground level. On the blackboard was a weather chart spanning thirteen winters, each column marked with local school closures and smoke advisories from factory districts nearby. The room had not been hidden from patients. It had been hidden from inspectors, preserving evidence that the hospital had tracked industrial illness in children years before the city acknowledged the cause.",
  ]),
  createStory("copper-bridge", "Story 26: The Copper Bridge Letters", "Epistolary drama", [
    "No one crossed Copper Bridge anymore because the bypass road was faster and the toll booths had long since been turned into planters. Yet every month the bridge authority still received one stamped envelope addressed simply to The Keeper, Copper Bridge, East Span.",
    "Archivist Joel was sent to close the account and reroute any lingering correspondence. The bridge office contained a desk, a steel kettle, a stack of repair manuals, and forty years of unanswered letters filed by river height. Most were written by people passing through. A few were written by the same hand every decade as if the sender expected the bridge itself to age more predictably than her life.",
    "The letters described brief meetings at the midpoint: a disagreement resolved during fog, a proposal interrupted by a toll horn, a promise to return after the harvest road was repaired. Joel noticed the dates corresponded with the bridge's copper expansion logs. The hottest days, when the span lengthened fractionally, were the same days the writer described arriving early and finding someone already waiting.",
    "On the final page of the most recent letter was a sketch of a hidden inspection hatch beneath the east rail. Joel opened it and found a narrow compartment lined with waxed envelopes, every one addressed back to the original writer but never sent. The keeper had been replying all along, leaving the letters inside the bridge so the river, the metal, and time itself could mediate what two people had not managed to say face to face.",
  ]),
  createStory("harvest-index", "Story 27: The Harvest Index", "Rural mystery", [
    "The cooperative's harvest index was meant to be practical: crop weights, transport loads, storage temperature, rainfall. But each year the book grew stranger, as though the clerks could not resist annotating abundance with gossip, resentment, and local memory.",
    "When agronomist Bela arrived to digitize the index, she built a spreadsheet and immediately lost confidence in numbers stripped from their margins. A peach shortfall made no sense until paired with a note about smoke from the west ridge. A sudden gain in millet output matched the year two families reconciled and reopened a shared threshing machine.",
    "The oldest pages included coded marks beside farms that no longer operated. Triangles, circles, and ink stars repeated every few seasons, but only in years when buyers from the export syndicate visited. Bela followed the symbols through decades of notebooks and realized they identified which farmers had quietly diverted part of their crop to the valley school and clinic during ration seasons.",
    "The present-day board wanted the data standardized and sanitized before investors saw it. Bela instead scanned the notebooks whole, stains and side comments included. Hidden in the mess was the actual resilience model of the valley: not just output, but who shared tools, who lent seed, and who kept people fed when official supply lines tightened. The harvest index had always been part ledger, part witness statement.",
  ]),
  createStory("opal-theater", "Story 28: The Opal Theater", "Performance mystery", [
    "The Opal Theater was famous for acoustics that made weak singers sound brave and for a ceiling mural no restoration budget could afford to properly clean. When stage manager Kian took the job, he expected late actors, broken pulleys, and donors with opinions. He did not expect nightly changes to the cue sheets in handwriting older than anyone on staff.",
    "The phantom revisions were subtle at first: shift lantern warm-up by two minutes, hold curtain longer after thunder cue, remove third chair from stage left. Each adjustment improved the scene it touched, but no rehearsal report took responsibility for them. The archivist eventually matched the handwriting to a former conductor who had died before the modern theater was built on the same site.",
    "As Kian traced the venue history backward, he learned the old opera house burned during a final performance cut short by civil unrest. Several musicians never made it out, and the replacement theater was erected so quickly that part of the old orchestra pit remained buried beneath the new stage rather than being demolished.",
    "On a rain-heavy dress rehearsal night, one actor missed an entrance because a floor panel jammed. Kian pried it loose and uncovered a stack of charred cue books wrapped in oilcloth. The ghostly edits in the modern prompt scripts matched annotations from those books line for line. Someone, or something, had been preserving the timing of the unfinished last performance by quietly correcting the living until the scenes could finally land the way they were meant to.",
  ]),
  createStory("violet-farm", "Story 29: Violet Farm", "Landscape mystery", [
    "The hillside lavender farm should have been simple inventory: row counts, bloom cycles, distillation runs, visitor bookings. Instead every field notebook contained side sketches of dry wells, ruined walls, and a path marked only with the phrase do not hurry here.",
    "Elin took over operations after her aunt's stroke and assumed the notes were sentimental. Then she noticed that the path sketches corresponded with patches where the lavender bloomed earlier and held scent longer into the evening. Soil tests found nothing unusual. Visitor photos, however, repeatedly captured a faint violet haze along the old terrace edge on windless days.",
    "The path led to a collapsed watch hut overlooking the river bend. Under its floorboards Elin found clay jars packed with seeds, map fragments, and a diary from the wartime caretaker who had hidden medicinal plants among the lavender rows to keep them from confiscation. The diary's sketches matched the notebook margins exactly. Her aunt had been maintaining the camouflage pattern all these years without ever writing it plainly.",
    "When the next tour group arrived, Elin almost redirected them from the marked trail. Instead she let them pass the terrace edge and smell the stronger blooms there, knowing they were brushing against a living archive of protective planting. The farm's beauty had never been incidental; it was the most durable cover story the hillside had ever grown.",
  ]),
  createStory("threshold-room", "Story 30: The Threshold Room", "Closing piece", [
    "In the municipal records building there was one room that never appeared on fire plans because it belonged to every department in theory and none of them in practice. Clerks called it the threshold room because forms passed through it when they were changing status: approved to denied, temporary to permanent, missing to found.",
    "When systems analyst Pranav was tasked with modernizing the filing workflow, he expected dusty shelves and territorial managers. Instead he found the threshold room meticulously ordered by categories no database schema could represent: unresolved but kind, corrected too late, forwarded without witness, returned by weather.",
    "The categories sounded absurd until he sampled the folders. Each one contained documents that had technically reached closure while leaving some emotional, civic, or moral residue behind. A bridge inspection cleared after the collapse it should have prevented. A teacher transfer approved only after the school term ended. An emergency grant denied in time to become a memorial fund instead.",
    "Pranav understood then why no department claimed the room. It was where bureaucracy stored the facts it could not absorb without becoming self-aware. He did not delete the categories when he built the new system. He hid them one layer deeper, naming the internal table threshold, because even in a cleaner digital workflow the city would still need a place for outcomes that arrived formally complete and yet remained unfinished to everyone who had to live with them.",
  ]),
];

export const APP_SIMULATORS = [
  {
    id: "document_reader",
    title: "Document Reader",
    description:
      "Long-form story reading, text selection, and content-heavy page navigation.",
    pages: [
      {
        id: "reader_volume_one",
        title: "Volume I",
        description:
          "The first long-form reading volume with ten stories for skimming, engaged reading, and deep reading.",
        sections: volumeOneStories,
      },
      {
        id: "reader_volume_two",
        title: "Volume II",
        description:
          "A second long-form volume with ten more stories for extended scroll depth and comparison behavior.",
        sections: volumeTwoStories,
      },
      {
        id: "reader_volume_three",
        title: "Volume III",
        description:
          "A slower final reading volume with ten extended stories suited to long dwell times and text selection.",
        sections: volumeThreeStories,
      },
    ],
  },
  {
    id: "task_manager",
    title: "Task Manager",
    description:
      "List-heavy productivity app with repeated check, move, and review actions across pages.",
    pages: [
      {
        id: "task_inbox",
        title: "Inbox",
        description:
          "Incoming tasks page for scanning, triaging, and clicking through short items.",
        variant: "tasks",
        tasks: [
          "Review new onboarding checklist",
          "Prepare weekly metrics summary",
          "Check support escalation notes",
          "Draft stakeholder update",
          "Compare budget revisions",
          "Revisit rollout timeline",
        ],
      },
      {
        id: "task_board",
        title: "Board",
        description:
          "Kanban-style planning page with more deliberate item review and lane switching.",
        variant: "board",
        columns: [
          { title: "Backlog", items: ["Audit event schema", "Review page navigation flow"] },
          { title: "In Progress", items: ["Label captured sessions", "Tune training split"] },
          { title: "Done", items: ["Add browser logging", "Expand page library"] },
        ],
      },
      {
        id: "task_calendar",
        title: "Calendar",
        description:
          "A scheduling page useful for page scanning, repeated clicks, and slower comparison.",
        variant: "calendar",
        slots: [
          "09:00 Review collector flow",
          "10:30 Label session set A",
          "12:00 Reader navigation capture",
          "14:00 Archive the long-form sessions",
          "16:00 Model retraining review",
        ],
      },
      {
        id: "task_analytics",
        title: "Analytics",
        description:
          "A summary page with throughput and backlog cards for quick glance vs slow inspection patterns.",
        variant: "task_analytics",
        metrics: [
          { label: "Tasks closed", value: "34" },
          { label: "Avg cycle time", value: "2.8d" },
          { label: "Blocked items", value: "5" },
          { label: "Reopened", value: "3" },
        ],
      },
    ],
  },
];
