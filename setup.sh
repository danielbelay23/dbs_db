mkdir -p ~/.streamlit/

cat <<EOF > ~/.streamlit/config.toml
[server]
headless = true
enableCORS = false
port = \$PORT
address = "0.0.0.0"

[theme]
primaryColor = "#ffcc00"
backgroundColor = "#1a1a2e"
secondaryBackgroundColor = "#2a2a3a"
textColor = "#e0e0e0"
font = "monospace"

[browser]
gatherUsageStats = false
EOF
