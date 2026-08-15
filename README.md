vektorcom-price-tracker/
│
├── .env                  <-- Hidden file: Stores private keys and webhooks (NEVER push to GitHub)
├── .gitignore            <-- Text file: Tells Git to ignore sensitive files like .env and logs
├── README.md             <-- Markdown file: The client-ready project documentation page
├── requirements.txt      <-- Text file: Lists your Python dependencies (Playwright, Requests, etc.)
│
├── config.py             <-- Python file: Safely loads your environment variables
├── tracker.py            <-- Python file: The main script that runs the automation loop
│
├── data/                 <-- Folder: Where local outputs are saved
│   └── tracker.db        <-- Database file: Local SQLite file storing scraped historical data
│
└── logs/                 <-- Folder: Keeps execution records organized
    └── tracker.log       <-- Log file: Records runs, successes, and browser errors
