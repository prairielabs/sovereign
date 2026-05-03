/*
 * PROJECT — Spur Demo
 * YouTube demo run of the Spur image generation system.
 * Read this file on session start after reset.
 */

define project spur_demo {

  name:    "Spur Demo"
  goal:    "Run Spur (apps/Spur.txt) with Tier 3 and Tier 4 executors. Record the run for YouTube."
  status:  "ready"
  tier:    "3 and 4 — track both, compare"
  created: "2026-04-29"

  description: """
  Simple demo run of Spur for a YouTube tutorial.
  No complexity. Load Spur. Make images. Record what happens.

  Spur is apps/Spur.txt — paste into Claude, type 'install Spur', then ask for images.
  The point of the demo: one .txt file turns a frontier model into an image generation system.
  """
}

define plan spur_demo {

  step: "1. Read apps/Spur.txt"
  step: "2. Install Spur in a fresh session (or dispatch to executor)"
  step: "3. Run 2–3 image generation prompts — document what Tier 3 and Tier 4 produce"
  step: "4. Write results to projects/spur-demo/results/"
  step: "5. Note any differences between Tier 3 and Tier 4 output quality/behavior"
}

define tracking spur_demo {

  // Log each run here as it happens.
  // Format: YYYY-MM-DD | tier | prompt | result | notes

  runs: []
}

define notes spur_demo {

  // OBS Studio install pending — need sudo in terminal:
  // sudo apt-get install -y obs-studio
  // Install before recording session.
}
