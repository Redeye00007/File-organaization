#!/bin/bash

echo "=== File Organizer for Termux ==="
echo "You can enter multiple folders separated by space"

# Read multiple folder paths
read -p "Enter folder paths to organize: " -a FOLDERS

for SOURCE_FOLDER in "${FOLDERS[@]}"; do
    if [ ! -d "$SOURCE_FOLDER" ]; then
        echo "Folder does not exist: $SOURCE_FOLDER"
        continue
    fi

    declare -A FILE_TYPES
    FILE_TYPES=( 
        ["Images"]="jpg jpeg png gif"
        ["Videos"]="mp4 mkv 3gp"
        ["Documents"]="pdf docx txt xlsx"
        ["Audio"]="mp3 wav"
        ["Archives"]="zip rar 7z"
    )

    echo "Organizing folder: $SOURCE_FOLDER"
    for FILE in "$SOURCE_FOLDER"/*; do
        if [ -f "$FILE" ]; then
            MOVED=false
            EXT="${FILE##*.}"
            EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')
            for FOLDER in "${!FILE_TYPES[@]}"; do
                for EXT_TYPE in ${FILE_TYPES[$FOLDER]}; do
                    if [ "$EXT_LOWER" == "$EXT_TYPE" ]; then
                        TARGET="$SOURCE_FOLDER/$FOLDER"
                        [ ! -d "$TARGET" ] && mkdir -p "$TARGET"
                        mv "$FILE" "$TARGET/"
                        echo "Moved: $(basename "$FILE") → $FOLDER"
                        MOVED=true
                        break 2
                    fi
                done
            done
            if [ "$MOVED" = false ]; then
                TARGET="$SOURCE_FOLDER/Others"
                [ ! -d "$TARGET" ] && mkdir -p "$TARGET"
                mv "$FILE" "$TARGET/"
                echo "Moved: $(basename "$FILE") → Others"
            fi
        fi
    done
    echo "Folder organized successfully: $SOURCE_FOLDER"
done

echo "=== All selected folders are organized! ==="
