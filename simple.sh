#!/bin/bash

while IFS=: read -r ip port; do
    ip=$(echo "$ip" | xargs)  # trim whitespace
    port=$(echo "$port" | xargs)
    
    filename="${ip}_${port}.html"
    
    echo "Connecting to $ip:$port..."
    
    s3270 -script <<EOF
Open($ip:$port)
Wait(2, Connected)
PrintText(string)
PrintText(html, $filename)
Quit()
EOF
    
    echo "Saved to $filename"
done < tn3270.txt
