+++
title = "Setting up gcloud for VertexAI credit usage"
date = 2025-01-29
draft = false

[taxonomies]
categories = ["Dev", "GCP", "VertexAI"]
tags = ["AI", "Setup"]

[extra]
lang = "en"
+++

1. Setup the GCP project and ensure you have enough credits
2. Run the following commands to configure it

```sh
pip install google-cloud-aiplatform
```

3. Install `gcloud`

```sh
sudo apt update && sudo apt install apt-transport-https ca-certificates gnupg curl -y

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
  sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
  sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

sudo apt update && sudo apt install google-cloud-sdk -y
```

4. Configure gcloud to let it use your credentials and allocate resources to your project

```sh
gcloud auth application-default login
```

This will open a web-browser, just login using google.

```sh
gcloud config set project YOUR_PROJECT_ID
```

You should be good to go now.