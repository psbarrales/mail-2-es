# Mail to Elasticsearch

Mail to Elasticsearch is a tool designed to extract email transactions from a Gmail mailbox and then store them in Elasticsearch. This application is particularly useful for those who need to perform detailed analysis of their email transactions, offering an efficient and automated method for collecting and storing such data.

## Features

- Automatic extraction of email transactions from Gmail.
- Stores transaction data in Elasticsearch for further analysis.

## Deploy on Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/qp9og6?referralCode=__wSQ2)

## Getting Started

This code is a resources made for the following post: [How I Improved My Personal Finances Using LLM](https://medium.com/@psbarrales/como-mejor%C3%A9-mi-econom%C3%ADa-personal-usando-llm-072bf5a6b7f7).

### Prerequisites

Before setting up Mail to Elasticsearch, ensure you have the following:

- A Gmail account with access to the mailbox from which you wish to extract transactions. 
- OpenAI API Key for the llm extraction feature.
- Telegram API Key and Chat ID for the notification feature.
- Docker
- python3 with pip

### Installation

1. Clone the repository to your local machine.
   ```
   git clone https://github.com/psbarrales/mail-2-es.git
   ```
2. Navigate into the project directory.
   ```
   cd mail-2-es
   ```
3. Install the required dependencies.
   ```
   pip install -r requirements.txt
   ```
4. Configure the application environment file .env, replace with your keys and settings:

```conf
    OPENAI_API_KEY=sk-aaa
    MAIL_USERNAME=dummy@dummy.com
    MAIL_PWD=zxcasdqwebnmjkliop
    TELEGRAM_TOKEN=TELEGRAM_TOKEN
    TELEGRAM_CHATID=TELEGRAM_CHAT_ID
    MAIL_BOX=Wallet
    ELASTICSEARCH_HOST=https://localhost:9200
    DATABASE_URI=postgresql+psycopg2://wallet:123DummyPass@localhost/wallet
```

### Running

To run all dependencies locally using Docker, execute:

```
docker-compose up
```

Then, to start the server, run:

```
python . --server
```

### Usage

To start extracting and storing make a curl to `/obtain_emails`:

```
curl -v -X GET http://0.0.0.0:8080/obtain_emails
```

### Kibana

To view your data you can open Kibana on `http://localhost:5601`

### Account Creation

To create an account make a POST curl to /account

```bash
curl -v -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "id": 99,
        "name": "Another - External",
        "billDate": "Same transaction date",
        "similarity": [
            "Any other account not listed"
        ],
        "primary": false
    }' \
    http://0.0.0.0:8080/account
```

### Tag Creation

The same for tag creation make a POST curl to /tag

```bash
curl -v -X POST \
    -H "Content-Type: application/json" \
    -d '{
    "tag": "Purchase",
    "description": "Any purchase of things",
    "similarity": ["Purchase..."]
  }' \
    http://0.0.0.0:8080/tag
```

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improving the application, please feel free to open an 'Issue' or submit a 'Pull Request'.

### How to Contribute

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

Mail to Elasticsearch is an open-source project under the MIT license. This license permits use, copying, modification, merging, publishing, distribution, sublicensing, and/or sale of copies of the software, provided that anyone who obtains a copy of this software and associated documentation files is granted permission to do so, always respecting the original copyright.
