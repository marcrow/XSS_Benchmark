#!/bin/bash

INPUT="app/scenarios/TBD/scenarios.yaml"
OUTPUT_DIR="app/scenarios/definitions"

mkdir -p "$OUTPUT_DIR"

current_file=""
content=""

# Regex pattern in a variable to avoid Bash parsing issues with < and >
filename_regex='^<!--[[:space:]]*(scenario_[0-9]+\.yaml)[[:space:]]*-->$'

while IFS= read -r line || [[ -n "$line" ]]; do
    # Check for filename comment using regex variable
    if [[ $line =~ $filename_regex ]]; then
        # If we have content from a previous scenario, write it out
        if [[ -n "$current_file" && -n "$content" ]]; then
            echo -e "$content" > "$OUTPUT_DIR/$current_file"
            content=""
        fi
        current_file="${BASH_REMATCH[1]}"
        continue
    fi

    # Check for scenario delimiter
    if [[ "$line" =~ ^---$ ]]; then
        # Write out the current scenario
        if [[ -n "$current_file" && -n "$content" ]]; then
            echo -e "$content" > "$OUTPUT_DIR/$current_file"
            content=""
            current_file=""
        fi
        continue
    fi

    # If we're inside a scenario, accumulate content
    if [[ -n "$current_file" ]]; then
        content+="$line"$'\n'
    fi
done < "$INPUT"

# Write the last scenario if file didn't end with ---
if [[ -n "$current_file" && -n "$content" ]]; then
    echo -e "$content" > "$OUTPUT_DIR/$current_file"
fi

echo "Extraction complete. Scenario files written to $OUTPUT_DIR"
