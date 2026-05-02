+++
title = "Scraping supreme court and High court data for CPT"
date = 2026-05-02
draft = false

[taxonomies]
categories = ["ML", "Scraping"]
tags = ["Fun", "Functional-programming"]

[extra]
lang = "en"
+++

I had been working on scraping some supreme court data to make it more accessible to the public. Like the data is there, but the website sucks, its slow, its **hard to pull** the legal records, especially if you know nothing about law (which I didn't).

> This data is available, openly accessible but not openly feasible

So my original goal was to make it feasible to access this. The way I thought about this was simple:

- I will scrape all the judgements and orders made by the Indian Supreme Court and all 25 Indian High Courts
- Then I will "somehow" (I didn't think how back then) link the relevant files together (most records reference other records)
- Create "some sort" of a database (no clue what or how) that will make this easier

Needless to say, there were a lot of variables and I don't like that. I was working for a few guys, and they came up with the idea of performing CPT (Continued Pre-Training) on a QWEN model with legal data to see if something cool happens (I think they wanted more than just **something cool** but that's how I took it).

## Building the supreme court data scraper

Few quriks, you are free to go and verify it for yourself, but I haven't added support for images on blogposts yet so unfortunately, I can't show you:

- This is the website in question, [SUPREME court](https://www.sci.gov.in) and [this is](https://www.sci.gov.in/judgements-judgement-date/) where the real scraping is going to happen because it allows us to search for all judgements within a timeframe.

- Instead of a dedicated, high-performance REST API, the site uses [https://www.sci.gov.in/wp-admin/admin-ajax.php](https://www.sci.gov.in/wp-admin/admin-ajax.php)

- The site does need auth via cookie sessions (trivial for any modern library).

- Once authentication is done, I just need to hit the `admin-ajax.php` page (I can quite literally see the) which is a POST request like this:

```py
"https://www.sci.gov.in/wp-admin/admin-ajax.php?from_date=DD-MM-YYYY&to_date=DD-MM-YYYY&scid=$REQUEST_VAL&siwp_captcha_value=$CAPTHCA_ANSWER&es_ajax_request=1&submit=Search&action=get_judgements_judgement_date&language=en"
```

- This returns a table with no pagination, you can take the HTML and you have everything that is needed.

Well I am making it sound more technical than it needs to be. The actual nail in the coffin for this experiement was that the PDFs are not signed or anything! So, once you have the URL for a PDF, say like this: https://api.sci.gov.in/supremecourt/2025/72357/72357_2025_12_14_70479_Judgement_23-Apr-2026.pdf, then you can open it anytime, from anywhere, without any auth.

This means if we can simply reconstruct the URL for all cases, then all we need to do is hit the `.pdf` links and we're done. Yeah, easier said than "done".

Look at this more carefully:

- https://api.sci.gov.in/supremecourt/2025/72357/72357_2025_12_14_70479_Judgement_23-Apr-2026.pdf
- https://api.sci.gov.in/supremecourt/2025/70109/70109_2025_3_1501_69876_Judgement_09-Apr-2026.pdf
- https://api.sci.gov.in/supremecourt/2025/68403/68403_2025_11_1501_69981_Judgement_07-Apr-2026.pdf

What's the pattern?

Probably something like:
```py
f"https://api.sci.gov.in/supremecourt/{year}/{num1}/{num1}_{year}_{num2}_Judgement_{judgement_day}-{judgement_mon}-{judgement_year}.pdf"
```

If we go and inspect the table we get:

```yaml
serial_number: 119
diary_number: 72357/2025
case_number: C.A. No.-006525-006525 - 2026
petitioner_respondent: CHALLANI GINNING AND PRESSING FACTORY VS KAMAL
petitioner_respondent_advocate: SANDEEP SUDHAKAR DESHMUKH

Bench: HON'BLE MR. JUSTICE SANJAY KUMAR HON'BLE MR. JUSTICE K. VINOD CHANDRAN HON'BLE MR. JUSTICE SANJAY KUMAR
```

Clearly, `num1` is the diary number and `year` is the diary year -> possibly when the case was registered. But were do we get the other numbers from? The goal is to find the `num2` value, because then we can brute force for 365 days a year for each year.

`num2` is clearly composed of 3 parts, `{smaller_part}_{medium_part}_{larger_part}`. These are definitely not RANDOM numbers, so let's dig into these. Some random guesses could be:

- Filing date?
- A sequence ID?
- Two of the cases shared the same medium_part => Some stable identifier for when, where or how?
- Judgement type?

---

Okay so I dug a little deeper, its easier than I thought. Take a look at this: [case-categories] https://www.sci.gov.in/case-category/. This clarifies the `num2` a little bit; `medium_part` is the case-category! (this can be useful in filtering the corpus later).

The elephant in the room is of-course the diary number. If there are no patterns in the diary-number then no point of doing this because we'll HAVE to solve the captcha and do all the session management to get the diary number, AT WHICH POINT, the pdf url is quite literally just there.

Anyway, this was a cool exploration. BTW, the larger part is most definitely the global sequence number. It possibly indicates the `zth` case that the court is seeing.

### Back to old route

The old path of session management via cookies and captcha solving is not as bad, but the problem is that the captchas, though are quite vanilla, cannot be decoded properly by traditional OCRs.

I tried, trust me, they don't work. I just need it to tell me what's there and I can call `eval` and solve the question via code. So, to do this, I went with the overkill solution: Running a QWEN2.5 VLM through vLLM on a Nvidia Spark.

I know, I know, but the guys I was working for happened to have one so why not. I set it up, once you install the necessary libraries and the model (I went with the 3B and not the 7B model cause **that** would be overkill!), and loaded it via a docker container:

```sh
docker run -it --gpus all     --ipc=host     --ulimit memlock=-1     --ulimit stack=67108864     -p 8000:8000     -v /home/collaborator/.cache/huggingface:/root/.cache/huggingface     -e VLLM_IMAGE_MAX_PIXELS=200704     nvcr.io/nvidia/vllm:26.02-py3     vllm serve Qwen/Qwen2.5-VL-3B-Instruct     --trust-remote-code     --max-model-len 1024     --max-num-seqs 1     --gpu-memory-utilization 0.25     --swap-space 0     --cpu-offload-gb 0     --limit-mm-per-prompt '{"image":1}'     --dtype bfloat16     --enforce-eager     --disable-log-requests
```

Notice all these flags? That's me trying to minimize memory usage. The 7B model (yeah I did try it, hehe) ended up taking a 100GB of RAM, this above one took only 20GB. Tested this out with an image of th (note that the API is exposed via OpenAI endpoints):

```sh
curl -s http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "Qwen/Qwen2.5-VL-3B-Instruct",
"messages": [
  {
    "role": "user",
    "content": [
      {"type": "text", "text": "Describe this image"},
      {"type": "image_url", "image_url": {"url": "https://commons.wikimedia.org/wiki/Tux_(mascot)#/media/File:Tux.png"}}
    ]
  }
],
"temperature": 0.0,
"max_tokens": 100
}' 
```

The goal obviously is to have this bad-boy gimme the OCR of the captcha and I will call eval and solve the problem and hit the right endpoints and scrape the data then the PDFs.

The actual code then is trivial to generate via an LLM, so I will not bother posting it here.

## High courts

I discovered something pretty funny about Bombay High Court (the website that is). I started with that. So, [this is the website](https://bombayhighcourt.nic.in/index.php) if you wish to follow along and laugh (not sure if they have changed stuff by the time this post reaches you)

BTW, pro-tip: If you are confused about where you can find certain things in a website, always hit the sitemap. Usually its `sitemap.xml`, but some old timers do `sitemap.php`.

[This](https://bombayhighcourt.nic.in/sitemap.php) is the bombay-high court sitemap. Now here we can see two things which are of interest to us:

1. Reported Judgments / Orders
2. Full Bench Judgments

Checking out [full bench judgements](https://bombayhighcourt.nic.in/judfbench.php) (these are basically those judgments made by the entire high court bench, all judges), we can clearly get all of them in a single non-paginated table.

-> Easy scrape

Checking the [reported Judgements / Orders](https://bombayhighcourt.nic.in/ord_qryrepact.php), a few things stand out:

1. There are about 11 different **sides** we'll have to account for while scraping
2. The **All act** is awesome cause no worrying about different acts then
3. The from date starts from 1966 (note that the Bombay High Court was formed in the mid 1800s).
4. There is a real captcha (like, not maths)

If you try to access 1966 data though, you'll see that the server errors out. This will keep happening until, 2005 (haha, basically they haven't digitalized previous records at all, but they **have** it I suppose). I actually verified this programmatically (very late in the game TBH) but now I am making it a practise to verify these kind of data sources.

The funniest part is the captcha. So, my initial plan was to again run QWEN2.5 3B on this and solve the captchas, BUT this is the URL being used to generate the captcha image:

```py
"https://bombayhighcourt.nic.in/bhccaptcha/captcha.php?rand=MS49TV"
```

> The URL contains the answer!

So, I simply have to read the image URL at that specific tag (`ID=captchaimg`) extract the "rand" part and that's the captcha answer.

Basically the way this captcha generation works, is that they have some algorithm that maps this post request to an image generation. Each letter corresponds to one of many ways to paste that on an image and the ordering is a fixed + random jitter of whitespace.

If you hit this URL now, and keep hitting refresh you'll keep getting slight variations of the same captcha. That's all there is to this.

This makes scraping super easy cause effectively, its just another param in the post request. Which brings us to the million dollar question:

### What is this post request like

To understand that, the easiest way is to hit the website on a proxy browser, I use burpsuite. When I do that, this is what I get:

```sh
POST /ordqryrepact_action.php HTTP/1.1
Host: bombayhighcourt.nic.in
Cookie: hidden=value; PHPSESSID=mhoive4k9v1v6ce3g4n3o29er1
Content-Length: 229
Cache-Control: max-age=0
Sec-Ch-Ua: "Not-A.Brand";v="24", "Chromium";v="146"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Accept-Language: en-GB,en;q=0.9
Origin: https://bombayhighcourt.nic.in
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://bombayhighcourt.nic.in/ord_qryrepact.php
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive

CSRFName=CSRFGuard_860672580&CSRFToken=5204e99c6c755f811e9d42f749b9338c9e3c376ba1a34bde700ae65810dd3717&pageno=1&frmaction=&m_sideflg=C&actcode=0&frmdate=01-04-2026&todate=01-05-2026&captchaflg=&captcha_code=9J59DH&submit1=Submit
```

The cookie is easy to capture via requests (you just need to make a get request before and handle the response), rest of the boiler plate will be handled by requests. The post fields are important:

```sh
CSRFName=CSRFGuard_860672580&CSRFToken=5204e99c6c755f811e9d42f749b9338c9e3c376ba1a34bde700ae65810dd3717&pageno=1&frmaction=&m_sideflg=C&actcode=0&frmdate=01-04-2026&todate=01-05-2026&captchaflg=&captcha_code=9J59DH&submit1=Submit
```

Let's see:

1. CSRFName and CSRFToken will both be handled via the HTTP session (we'll need `httpx.Client` for this now)
2. `m_sideflg` is a field we'll need to keep an eye on
3. Rest all are cool

Why did I flag `m_sideflg`? Because I am currently hitting only one of the `sides` from above. We have 11, so I am assuming (and correctly) that each of these have a unique code. The best way is to capture 11 post requests and ensure that we have a proper mapping for each so that scraping is much easier later. This is what I found:

```py
SIDE_TO_FLAG = {
"Bombay- Appellate(Civil)":    "C",
"Bombay- Appellate(Criminal)": "CR",
"Bombay-Original":             "OS",
"Nagpur-Civil":                "NC",
"Nagpur-Criminal":             "NR",
"Aurangabad-Civil":            "AC",
"Aurangabad-Criminal":         "AR",
"Goa-Civil":                   "GC",
"Goa-Criminal":                "GR",
"Kolhapur-Civil":              "KC",
"Kolhapur-Criminal":           "KR",
}
```

Then we can set from date to 2005 1st Jan and start extracting. (Note that, I tried to hit the server with the date formatted as `DD/MM/YYYY` and got a nasty **501** with no indication of what was wrong. So make sure you send it as `DD-MM-YYYY`)

### A quirk about the PDF downloading

So these guys have done something interesting with the PDF links, they have a centralized router: `/generatepdf.php?bhcpar=<base64_string>`. When you decode the bhcpar string, it’s not an encrypted token or a 
database hash; it is literally just another standard query string: `path=...&fname=...&uploaddt=....`.

They took perfectly normal URL parameters and base64-encoded them to make them look like a secure token. Well, anyways, not that big of a deal I suppose.

So that is all there is to scraping Bombay High Court data. That's like 200k+ PDFs, luckily the spark has enough space (1TB).

Next up is probably Delhi High Court.