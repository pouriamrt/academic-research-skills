#!/usr/bin/env bash
# beep.sh — Cross-platform audible alert for pipeline checkpoints and human-in-the-loop pauses.
# Usage: bash tools/beep.sh
#
# Plays three ascending tones (~2 seconds total): 800Hz → 1000Hz → 1200Hz.
# Used by: pipeline_orchestrator_agent (checkpoint alerts), execution_engine_agent (Colab GPU pause).

case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*|Windows_NT)
        # Windows (Git Bash / MSYS2 / Cygwin)
        powershell -c "[console]::beep(800,400); Start-Sleep -m 200; [console]::beep(1000,400); Start-Sleep -m 200; [console]::beep(1200,600)"
        ;;
    Darwin)
        # macOS
        osascript -e 'beep 3'
        ;;
    Linux)
        # Linux — try paplay (PulseAudio), then speaker-test, then terminal bell
        if command -v paplay &>/dev/null; then
            for freq in 800 1000 1200; do
                paplay --raw --rate="$freq" --channels=1 /dev/urandom &
                pid=$!
                sleep 0.3
                kill "$pid" 2>/dev/null
            done
        elif command -v speaker-test &>/dev/null; then
            for freq in 800 1000 1200; do
                (speaker-test -t sine -f "$freq" -l 1 &) 2>/dev/null
                sleep 0.3
                kill $! 2>/dev/null
            done
        else
            # Fallback: terminal bell (3 times)
            printf '\a'; sleep 0.3; printf '\a'; sleep 0.3; printf '\a'
        fi
        ;;
    *)
        # Unknown platform — terminal bell fallback
        printf '\a'; sleep 0.3; printf '\a'; sleep 0.3; printf '\a'
        ;;
esac
