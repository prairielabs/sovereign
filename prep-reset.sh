#!/usr/bin/env bash
# prep-reset — Sovereign session shutdown procedure
# Run before ending a session to write state and flush volatile memory.
# Usage: ./prep-reset.sh

SOVEREIGN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M")
DATE=$(date +"%Y-%m-%d")

echo "=== Sovereign prep-reset ==="
echo "Timestamp: $TIMESTAMP"
echo "Dir: $SOVEREIGN_DIR"
echo ""

# 1. Flush RAM.md
echo "Flushing RAM.md..."
cat > "$SOVEREIGN_DIR/RAM.md" << 'EOF'
/*
 * RAM — Sovereign
 * Volatile scratchpad. Flushed each session.
 * Nothing here survives reset.
 */

// Empty.
EOF
echo "  ✓ RAM.md flushed"

# 2. Update WORKING.md last_session_end timestamp
echo "Updating WORKING.md session end..."
sed -i "s/last_session_end:  \".*\"/last_session_end:  \"$TIMESTAMP\"/" "$SOVEREIGN_DIR/WORKING.md"
echo "  ✓ WORKING.md updated (last_session_end: $TIMESTAMP)"

# 3. Print reminder for Sovereign to write session notes
echo ""
echo "=== Manual steps for Sovereign ==="
echo "  1. Append session note to WORKING.md session_notes block:"
echo "     $DATE — <one-line summary>"
echo "  2. Write memory to: memory/$DATE.md"
echo "  3. Confirm loop/tasks/ and loop/reports/ are written for this session"
echo ""

# 4. Show loop artifact count
TASK_COUNT=$(ls "$SOVEREIGN_DIR/loop/tasks/" 2>/dev/null | wc -l)
REPORT_COUNT=$(ls "$SOVEREIGN_DIR/loop/reports/" 2>/dev/null | wc -l)
echo "=== Loop state ==="
echo "  Tasks on disk:   $TASK_COUNT"
echo "  Reports on disk: $REPORT_COUNT"
echo ""

echo "=== prep-reset complete ==="
echo "Session state written. Safe to reset."
