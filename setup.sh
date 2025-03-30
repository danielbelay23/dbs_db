mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
address = \"0.0.0.0\"\n\
[theme]\n\
primaryColor = \"#ffcc00\"\n\
backgroundColor = \"#1a1a2e\"\n\
secondaryBackgroundColor = \"#2a2a3a\"\n\
textColor = \"#e0e0e0\"\n\
font = \"monospace\"\n\
[browser]\n\
gatherUsageStats = false\n\
" > ~/.streamlit/config.toml