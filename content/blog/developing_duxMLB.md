+++
title = "Developing duxMLB, an extension for MLB fans"
date = 2025-01-29
draft = false

[taxonomies]
categories = ["AI", "Software"]
tags = ["Python", "yolo", "Deep learning"]

[extra]
lang = "en"
+++

This is how I built duxMLB and what it really is. It was developed for a hackathon and though I eventually got bored I decided to finally finish it and write about it. The following is the elevator pitch that I gave for the official submission.

## Inspiration

I found this hackathon through a friend and I figured something very interesting can be done with this problem statement. Around a week before the launch of this hackathon I was working on an AI based terminal, which I called `TerminAI`. It was a LAM type framework where the user could enter their commands in natural lanaguge (and not bash or MAC commands) and have it execute. So, things they didn't know how to do using a normal terminal could be done there. So, I was pretty much `into` the idea of creating LAM based applications because I found normal LLMs to be pretty boring and overdone.

When I heard of this, the first thing that came to my mind was a **live statcast generator**, that would record your screen realtime and generate data based on that. This was the time when Apple Intelligence was also gaining some hype and it did something similar so I figured I would do this. But soon I realised that, though it make for a **good project**, it would've been pretty useless cause nowadays statcast data is present during games! 

To figure what to build, I watched some games and I had never watched baseball before so it took time to figure out the rules and man I got hooked! I won't go into my watching spree cause that's probably not needed but it was a fun time. However, I found myself constantly searching for players and teams so the best place to start with seemed like a **simple LLM** that I can type the player's name and get information. And morever it had to be `while` I was watching the games cause I didn't want to open new tabs! So, therefore the idea of a `chrome extension` came to me.

Since then, I have included a lot more functionality to my extension (catering to the given problem statements) and I decided to call it `duxMLB` that is `Captain of MLB` in Latin (I like to have fun with names). The next few sections will explain more details about this extension.

## What it does

The following are the features that **duxMLB** shows:

1. A panel on the side for you are watching live matches. It is `Gemini` instructed to be a `good baseball coach` and answer related questions.

- It has three API calls that it can make. Firstly to get `player information`, secondly for `team information` and lastly for getting the `schedule`. 
- The user can normally interact with it, and when they ask for any of the three above, the LLM calls an API and gets the results.
- The results are pretty printed through another Gemini model (that I call the `pretty_printer`).

2. The panel also allows users to get the last `5 seconds of video` they were watching and generate statcast data for that.

- The timing is crucial for this and the implementation is also pretty slick. I will explain how this works in the next section.
- The `statcast` data generated is basically just two things:

	- Pitch speed
	- Bat swing speed

- If there is no such **pitches** or **swings** in those 5 seconds then it will output nothing basically.

3. Then there is the `options` page. Here there are 3 things:

- The first is the **MLB future predictor** which takes in the `homerun` data for the user and based on similarities with the top players, it tells the user how good or bad they are.
- This comparision is done using a dataset that was provided with the problem statement itself and a `vectorDB`.

- There is a guide page that also goes into the implementation and functionality (I didn't know I would have to write here as well, so I was planning to use that as a guide)

- Finally there is a classics video/name uploader which users can use to upload their favourite games, and generate statcast data for that. Again statcast data means 
	- Pitch speed
	- Bat swing speed
- If the user doesn't have the video with them locally (which is usually going to be the case), they can simply enter the name and it will be scraped.

So, I have tried to develop mulitple functionalities mentioned in the problem statement into one product. I had a lot more things in mind, but I will talk about them in another section.

## How I built it

### The overview

First I will talk about the panel. The GUI is pretty basic, and built using plain `HTML`, `CSS` and `JS`. This is because I have little experience with web development, and the basic technologies are something I understand and can debug. There is a `flask` backend that supports this, flask because its pretty easy to set up and I haven't learnt django or other python based web frameworks.

There is one `main` file which contains all the necessary endpoints. The `background.js` and `content.js` javascripts are responsible for figuring out when the extension is supposed to be clickable and used. This happens only for websites that have a `youtube.com` in them (basically YouTube). We can extend this to other MLB streaming channels as well, but for a hackathon run YouTube works the best. 

The `options page` for the extension which contains the other features also has a simple UI. I have added three functionalities to it for which I used a host of technologies like `pinecone`, a **vector database** for similarities and `selenium` for **web scraping**. There is also a guide page which explain what this website is about and some tehcnical implementations. 

In the coming subsections I will talk majorly about the backend and now the UI because that is pretty normal stuff and nothing interesting.

### The flow

This is how the website flow works:

{{ figure(src="assets/duxMLB_flow.png", alt="duxMLB flow diagram", caption="Flow diagram") }}

### Building the live statcast setup

This setup is the one where you can type "How fast was that swing?" in the panel and get accurate results. This is the code the helps me get the video feed and store it in a `rolling buffer`. This is the `content.js` script basically.

```js
function captureVideo() {
    const videoElement = document.querySelector("video"); // We're targeting the video element in YouTube

    if (!videoElement) {
        console.error("No video element found!");
        return;
    }

    // Setting up the canvas to store the video frames
    // I have set the FPS at 30 approx for the videos (which is more or less valid)
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    // Starting to capture frames
    const captureInterval = setInterval(() => {
        if (videoElement.paused || videoElement.ended) {
            clearInterval(captureInterval);
            return;
        }

        // This is drawing the current video frame to the canvas
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        // We need to convert this canvas to a Blob and then store it in the buffer
        canvas.toBlob((blob) => {
            if (buffer.length < BUFFER_SIZE) {
                buffer.push(blob);
                console.log("Added new frame at index:", buffer.length - 1);
            } else {
                console.log("Overwriting frame at index:", bufferIndex);				// This is the rolling part that saves only 5 seconds of video feed
                buffer[bufferIndex] = blob;
                bufferIndex = (bufferIndex + 1) % BUFFER_SIZE;
            }
        }, "image/webp"); // We're saving individual frames as webp images
    }, 1000 / FRAME_RATE);
}

// This is a trigger for the play button. As soon as that is clicked, you can head over to inspect/console to view the frames in the logs.
document.addEventListener("play", (event) => {
    if (event.target.tagName === "VIDEO") {
        console.log("Video playback started. Initializing capture...");
        captureVideo();
    }
}, true);
```

This buffer is then sent to the endpoint `/process-video` to the flask backend, where I store this buffer locally, then run my statcast models on it and give an output. The running time for all of this is around 1sec/frame which translates to 150 seconds for a 5 second video (in a corei5 10th gen HP laptop, if you have a better core then you're lucky).

### Integrating the APIs

The panel can query APIs based on the user's request. The main code that does this resides in the `API_querying` directory of the `backend` in a file called `query.py`. This is a `multi-model structure` where the user first goes through a Gemini model used to detemine if API calls are needed. This is determined by figuring out if the user is asking for either

1. Player's data
2. Team's data
3. MLB schedule

The thing with the API calls was that the URLs expected the `codes` that is, a numerical value rather than a string for the names. Thus, I first scraped the data using `requests` and `beautiful soup` and created a mapping for the team's and player's name to their official codes as expected by the API URLs. Thus the model returns a tuple object that I called `name_code_tuple` which contains information on whether this was a **player call**, **team call** or **schedule call** and the relevant code.

```python3
def call_API(name_code_tuple, year=2025, game_type='R'):
	assert type(name_code_tuple) == tuple, 'Maybe you made a mistake in the name? Check your spellings please! I am doing this all manually, an AI can get tired!'
	type_, code = name_code_tuple

	if type_ == code: 			# That is both are schedule, we're gonna assume 2024 for now, later we can add the yaer as well
		url_1 = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={year}&gameType={game_type}"
		webpage = requests.get(url_1, headers=headers).text

		schedule = parse_schedule(webpage)
		analysis = get_schedule_analysis(schedule)
		print_schedule_summary(analysis)
		return output_		

	if 'player' in type_:	 		# No need to go lower and all here, I have myself defined this

		# This is the relevant url for the player's data
		url_4 = f"https://statsapi.mlb.com/api/v1/people/{code}"
		webpage = requests.get(url_4, headers=headers).text

		# Now parse this
		players = parse_player_data(webpage)

		_output_ = """"""  										# ensuring this is empty
		for player in players:
			_output_ += f"""\nPlayer Information:
\nName: {player.full_name} \nPosition: {player.primary_position.name} \nBirth Date: {player.birth_date.strftime('%B %d, %Y')} \nFrom: {player.birth_city}, {player.birth_state_province}, {player.birth_country} \nBats: {player.bat_side.description} \nThrows: {player.pitch_hand.description} \nDraft Year: {player.draft_year} \nMLB Debut: {player.mlb_debut_date} \nLast Played: {player.last_played_date} \nActive: {player.active} \nNick_name: {player.nick_name} \nName_slug: {player.name_slug} \nBat_side: {player.bat_side} \nTop strike zone: {player.strike_zone_top} \nPitch hand: {player.pitch_hand} \nGender: {player.gender} \nPrimary position: {player.primary_position} \nPrimary number: {player.primary_number} \nCurrent age: {player.current_age}
			"""
		return _output_

	elif 'team' in type_:
		output = "" 				# we'll write everything we print here
		url_2 = f"https://statsapi.mlb.com/api/v1/teams/{code}/roster?season={year}"

		json_str = requests.get(url_2, headers=headers).text
		roster = parse_roster_data(json_str)
		# Get analysis
		analysis = get_roster_analysis(roster)

		output += f"Total players: {analysis['total_players']} \n"
		output += f"Active players: {analysis['active_players']} \n"
		output += f"Position breakdown:\n"

		for pos, count in analysis['positions'].items():
			# print(f"{pos}: {count}")
			output += f"{pos}: {count} \n"
		output += "\nStatus breakdown:"

		for status, count in analysis['status_breakdown'].items():
			output += f"{status}: {count} \n"
		active_pitchers = [p for p in roster if p.status == PlayerStatus.ACTIVE.value and p.position.type == "Pitcher"]
		output += "\nActive pitchers:"

		for pitcher in active_pitchers:
			output += f"{pitcher.full_name} (#{pitcher.jersey_number}) \n"
		return output
	else:
		output = "Nah, shoudn't come here at all. Just for safety"
		return output
```

Then we query the relevant URL based on this tuple and pass the acquired output through another `Gemini` model for pretty printing. I have tried to make things easy for this model by defning my own `dataclasses` and essentially parsing each acquired content through the APIs and storing them in a single output variable which is then pretty printed.

### Calculating bat speed

I first tried to train my own model which was a big problem (as I have described in the next section) because the datasets I found online for `baseball tracking` were not exactly representative of a pitcher throwing a pitch and hence detection stats were very bad. Then I found this [GitHub repo](https://github.com/dylandru/BaseballCV) which I ended up using for the final run. It came with pretrained weights for a YOLO model, on baseballs specific to those thrown in a **MLB setting** by a **pitcher**.

The following underlines how the speed calculation works: (assuming that the input video is of a pitcher throwing the ball)

1. The video feed is broken down into different frames based on the FPS for the video and the total duration.
2. The model detects the baseball in each frame and stores its **center's coordinates in the pixel dimension** to a buffer. 
3. After the detections are done for the baseball, we run a **different model to detect the pitcher and catcher** in each frame and calculate their average positions during the pitch.
4. The real distance between the pitching mount and catcher is around 60 to 61 feets. The calculated average distance between them in pixels is correlated with the real distance to find the `pixel_to_feet_ratio`.
5. The positions of the ball are then made into **valid sequences**. These are sequences of __consecutive__ baseball detections in between frames (or with at max 2 missing detections in between valid detections) and these are testament to the baseball actually being pitched.
6. For each valid sequence, we find the total distance it travelled in pixel coordinates in the X and Y directions (X,Y being the normal coordinate system) and calculate the average velocities in X and Y direction.
7. We then calculate the parabolic average velocity and use the pixel_to_feet_ratio to convert this in ft/s.
8. Next we correct for the camera angle using the angle made by the `pitcher and catcher to the normal` (that is, the line that splits the screen vertically) when the catcher acts a pivot to the normal line (so, we first **shift the entire pitcher and catcher line mathematically**). The math suggests that we calculate this angle using `beta = float(np.arctan(2*(x1-x2)/(y2-y1)))` where x1,y1,x2,y2 are average coordiantes of the pitcher and the catcher.

I have only used this angle if it is less than 10 degrees, because I found that only then are the results accurate enough (otherwise for larger angles, you don't really need this as frame by frame calculation is good enough there). The corrected velocities are then the predicted ones divided by the sine of this angle.
```py
def calculate_speed_ball(video_path, min_confidence=0.5, max_displacement=100, min_sequence_length=7, pitch_distance_range=(55,65)):
    SOURCE_VIDEO_PATH = video_path

    coordinates = calculate_pitcher_and_catcher(SOURCE_VIDEO_PATH)                     # Returns coordinates as (x1, y1, x2, y2)    
    x1, y1, x2, y2 = coordinates

    scale_factor = float(np.sqrt((x2-x1)**2 + (y2-y1)**2)/(60.5))              # scale factor is pixel distance between those guys divided by actual distance between the niggas
    beta = float(np.arctan(2*(x1-x2)/(y2-y1)))                              # The math is explained in the readme docs (UPDATE IT)

    load_tools = LoadTools()
    model_weights = load_tools.load_model(model_alias='ball_trackingv4')
    model = YOLO(model_weights)

    tracker = BaseballTracker(
    model=model,
    min_confidence=0.3,         # 0.3 confidence works good enough, gives realistic predictions
    max_displacement=100,       # adjust based on your video resolution
    min_sequence_length=7,
    pitch_distance_range=(60, 61)  # feet
    )

    print('processing video')
    results = tracker.process_video(video_path, scale_factor) 

    output = """"""

    output += f"\nProcessed {results['total_frames']} frames at {results['fps']} FPS" + f"\n Found {len(results['sequences'])} valid ball sequences"

    for i, speed_est in enumerate(results['speed_estimates'], 1):
        # Run the beta calculations for each frame
        output += f"""
            \nSequence {i}:
            Frames: {speed_est['start_frame']} to {speed_est['end_frame']}
            Duration: {speed_est['time_duration']:.2f} seconds
            Average confidence: {speed_est['average_confidence']:.3f}\n
        """

        estimated_speed_min = float(speed_est['min_speed_mph'])
        estimated_speed_max = float(speed_est['max_speed_mph'])

        if beta*180/3.1415926 > 10:                               # if the angle is less than 10 degree, then the calculations become absurd!
            v_real_max = estimated_speed_max * 1/np.sin(beta)                    # This necessarily implies that v_real is more than v_app which is true.
            v_real_min = estimated_speed_min * 1/np.sin(beta)
            output += f"\nEsttimated speed: {v_real_max:.1f}" + f" to {v_real_min:.1f} mph"

        else:
            output += f"\nEstimated speed: {estimated_speed_min:.1f}" + f" to {estimated_speed_max:.1f} mph \n"
            print(f'Estimated speed range: {estimated_speed_max, estimated_speed_min}')

        output += f"This was within the time frame: {speed_est['start_frame'] * 1/results['fps']} to {speed_est['end_frame'] * 1/results['fps']}"

    return output
```

### Bat swing speed calculation

These are the steps following to calulate the maximum swing speed:

1. The video is broken into different frames based on FPS and total duration. 
2. The `bat detection model` runs in each frame and stores the coordinates of the bat in a list.
3. The `pixel_to_ft_ratio` is calculated for the video using the bat length in pixel coordinates divided by that in real life.
4. The detections for the bat are passed to a `univariate spline` to get a continous detection sequence. I then differentiate this spline using small time intervals and find the maximum speed.

## Challenges I ran into

-- Getting the buffer feed
-- Finding the right model for baseball tracking (and training my own)
-- The math for the camera correction
-- Hosted backend on render but it ran out of memory

## Accomplishments that I am proud of

-- Multi-model structure
-- Multiple simultaneous architecture

## What I learned

-- First time using DL stuff
-- Building this was fun!

## What's next for duxMLB

Lot of things to write here!

-- Get users to upload their swings and compare with MLB swings
-- Host it up so you don't have to run the python file again and again
-- Since we are already detecting pitchers and catchers, we can do similar things for other players and then based on where they are standing, figure out what sort of game is being played

The reason I didn't do this is because I had absolutely no idea what type of games exist. (give them how to make it though)