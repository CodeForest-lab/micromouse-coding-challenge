#!/bin/bash

MAZE=$1
SOL_DIR=$2

if [ -z "$MAZE" ] || [ -z "$SOL_DIR" ]; then
    echo "Usage: $0 <maze_folder> <solutions_folder>"
    exit 1
fi

TMP_FILE="results_tmp.txt"
> "$TMP_FILE"

for sol in "$SOL_DIR"/*.py; do
    NAME=$(basename "$sol" .py)

    python maze.py --run "$MAZE" --solution "$sol" > /dev/null

    FILE="team_${NAME}.txt"

    if [ -f "$FILE" ]; then
        SCORE_LINE=$(head -n 1 "$FILE")
        PHASE1=$(echo "$SCORE_LINE" | cut -d',' -f1)
        PHASE2=$(echo "$SCORE_LINE" | cut -d',' -f2)

        echo "$NAME,$PHASE1,$PHASE2" >> "$TMP_FILE"
    else
        echo "$NAME,-1,-1" >> "$TMP_FILE"
    fi
done

# echo ""
# echo "🏆 Leaderboard (sorted by Phase 2):"
# echo "----------------------------------"

# sort -t',' -k3 -n "$TMP_FILE" | while IFS=',' read NAME P1 P2; do
#     printf "%-20s Phase1=%-6s Phase2=%-6s\n" "$NAME" "$P1" "$P2"
# done

rm "$TMP_FILE"