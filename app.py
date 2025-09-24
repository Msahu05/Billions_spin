from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
import random

app = Flask(__name__)

# Character data for 30 characters
WHEEL_DATA = [
    {
        "id": 1,
        "image": "img1.png",
        "char_image": "char1.png",
        "title": "Javi.eth",
        "x_username": "@jgonzalezferrer"
    },
    {
        "id": 2,
        "image": "img2.png",
        "char_image": "char2.png",
        "title": "Salesman 24/7",
        "x_username": "@salesman_1k"
    },
    {
        "id": 3,
        "image": "img3.png",
        "char_image": "char3.png",
        "title": "Adri 💜",
        "x_username": "@web3_adri"
    },
    {
        "id": 4,
        "image": "img4.png",
        "char_image": "char4.png",
        "title": "Star Jessie",
        "x_username": "@StarJessie_web3"
    },
    {
        "id": 5,
        "image": "img5.png",
        "char_image": "char5.png",
        "title": "Senorita.Dutt64",
        "x_username": "@senorita_dutt64"
    },
    {
        "id": 6,
        "image": "img6.png",
        "char_image": "char6.png",
        "title": "MIA 🩷",
        "x_username": "MiaLuvs2Build"
    },
    {
        "id": 7,
        "image": "img7.png",
        "char_image": "char7.png",
        "title": "Lulu 💜",
        "x_username": "@LouyemaLo"
    },
    {
        "id": 8,
        "image": "img8.png",
        "char_image": "char8.png",
        "title": "Eren",
        "x_username": "@dhruv9518"
    },
    {
        "id": 9,
        "image": "img9.png",
        "char_image": "char9.png",
        "title": "HoneyBit.eth",
        "x_username": "@infinity_max"
    },
    {
        "id": 10,
        "image": "img10.png",
        "char_image": "char10.png",
        "title": "Dashke",
        "x_username": "@Dashke_witch"
    },
    {
        "id": 11,
        "image": "img11.png",
        "char_image": "char11.png",
        "title": "Kovac",
        "x_username": "@Mr_Kovacs"
    },
    {
        "id": 12,
        "image": "img12.png",
        "char_image": "char12.png",
        "title": "Fave 🥶💙",
        "x_username": "@IceyEiza"
    },
    {
        "id": 13,
        "image": "img13.png",
        "char_image": "char13.png",
        "title": "oleh8",
        "x_username": "@oleh26591"
    },
    {
        "id": 14,
        "image": "img14.png",
        "char_image": "char14.png",
        "title": "TRUTH 🧑‍🍳",
        "x_username": "@heistruthX"
    },
    {
        "id": 15,
        "image": "img15.png",
        "char_image": "char15.png",
        "title": "Hizzy 🧡🦺",
        "x_username": "@hizzy_tonlover"
    },
    {
        "id": 16,
        "image": "img16.png",
        "char_image": "char16.png",
        "title": "Kaval P⚜",
        "x_username": "@okeykavall"
    },
    {
        "id": 17,
        "image": "img17.png",
        "char_image": "char17.png",
        "title": "MonicaTalan",
        "x_username": "@monitalan"
    },
    {
        "id": 18,
        "image": "img18.png",
        "char_image": "char18.png",
        "title": "Tajudeen",
        "x_username": "@Tajudeen_10"
    },
    {
        "id": 19,
        "image": "img19.png",
        "char_image": "char19.png",
        "title": "Jules 🦋",
        "x_username": "@Julesofhertime"
    },
    {
        "id": 20,
        "image": "img20.png",
        "char_image": "char20.png",
        "title": "Holly",
        "x_username": "@holly_web3"
    },
    {
        "id": 21,
        "image": "img21.png",
        "char_image": "char21.png",
        "title": "Gigi 🫶✨",
        "x_username": "@G1G1_Verse"
    },
    {
        "id": 22,
        "image": "img22.png",
        "char_image": "char22.png",
        "title": "Moonraker⚔",
        "x_username": "@rakermoon89"
    },
    {
        "id": 23,
        "image": "img23.png",
        "char_image": "char23.png",
        "title": "Yelyzaveta",
        "x_username": "@xsx_lisa"
    },
    {
        "id": 24,
        "image": "img24.png",
        "char_image": "char24.png",
        "title": "THANOS 24/7",
        "x_username": "@Thanos_24_7"
    },
    {
        "id": 25,
        "image": "img25.png",
        "char_image": "char25.png",
        "title": "Yuki Rex",
        "x_username": "@yuki_himanshu"
    },
    {
        "id": 26,
        "image": "img26.png",
        "char_image": "char26.png",
        "title": "OKES",
        "x_username": "@horkays"
    },
    {
        "id": 27,
        "image": "img27.png",
        "char_image": "char27.png",
        "title": "~Mikasa 🔯💜",
        "x_username": "@Chinwa01"
    },
    {
        "id": 28,
        "image": "img28.png",
        "char_image": "char28.png",
        "title": "Jazz_z_man",
        "x_username": "@Jazz_a_man"
    },
    {
        "id": 29,
        "image": "img29.png",
        "char_image": "char29.png",
        "title": "Jeff",
        "x_username": "@web3_tech_"
    },
    {
        "id": 30,
        "image": "img30.png",
        "char_image": "char30.png",
        "title": "Sophy",
        "x_username": "@KentBrenna80675"
    }
]


# Challenge pool - add more challenges as needed
CHALLENGES = [
    "I challenge you to create a meme video on javi and quote it to this post.",  
    "I challenge you to create a new and unique super mask for the billions community and quote it to this post.",  
    "I challenge you to share your billions community journey and quote it to this post.",  
    "I challenge you to write some good points about this character and mention them and also quote it to this post.",  
    "I challenge you to make a video of yourself saying 'Billions Has The Best Community' and quote it to this post.",  
    "I challenge you to speak in any Billions Community Space and tell us about your experience and quote it to this post.",  
    "I challenge you to make an edit on Billions Community Creators and quote it to this post.",  
    "I challenge you to upload a selfie photo with a new billions supermasks and quote it to this post.",  
    "I challenge you to upload a selfie video with a new billions supermasks and quote it to this post.",  
    "I challenge you to make an info post about all the mods of Billions Community and quote it to this post.",  
    "I challenge you to share your discord messages count of billions channel and quote it to this post.",  
    "I challenge you to create a poster showing big creators of billions and quote it to this post.",  
    "I challenge you to make a video saying 'Stay Bullish On Billions Network' and quote it to this post.",  
    "I challenge you to share your best content again and quote it to this post.",  
    "I challenge you to make a meme on Star_Jessie or Lulu or Hizzy or Tajudeen {Any one of them} and quote it to this post.",  
    "I challenge you to draw a billions logo using pen and paper and quote it to this post.",  
    "I challenge you to showcase your talent {Any type of Talent} and quote it to this post.",  
    "I challenge you to prank any community members and share about that and quote it to this post.",  
    "I challenge you to make a video on Hizzy's latest hook step and quote it to this post.",  
    "I challenge you to make a post on Eren {@dhruv9518} and quote it to this post.",  
    "I challenge you to create a video and inspire others about Billions Network and quote it to this post.",
    "I challenge you to make a twerk video and quote it to this post."
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/api/wheel-data')
def get_wheel_data():
    return jsonify(WHEEL_DATA)

@app.route('/api/item/<int:item_id>')
def get_item(item_id):
    item = next((item for item in WHEEL_DATA if item['id'] == item_id), None)
    if item:
        # Add random challenges to the character data
        random_challenges = random.sample(CHALLENGES, 2)
        character_with_challenges = item.copy()
        character_with_challenges['challenges'] = random_challenges
        return jsonify(character_with_challenges)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/challenges')
def get_challenges():
    """Return 2 random challenges"""
    return jsonify({"challenges": random.sample(CHALLENGES, 2)})

# Serve static files
@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/static/characters/<filename>')
def serve_character(filename):
    return send_from_directory('static/characters', filename)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/characters', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=8080)