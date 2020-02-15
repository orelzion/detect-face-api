
from flask import Flask
from flask import request
from flask import jsonify
import requests
import operator

FACE_API = "https://francecentral.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=emotion&recognitionModel=recognition_01&returnRecognitionModel=false&detectionModel=detection_01"

app = Flask(__name__)

@app.route('/face/detect', methods=["POST"])
def detectFace():
    if request.headers['Content-Type'] == 'application/octet-stream':
        faceDetectResponse = callFaceApi(request.data)
        return extractFaceResponse(faceDetectResponse)
    else:
        return "415 Unsupported Media Type ;)"

def callFaceApi(imageData):
    headers = {'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': '4b92ec68f063442198447acff4dbe07a'}
    response = requests.post(FACE_API, headers = headers, data = imageData)
    return response.json()

def extractFaceResponse(rawResponse):
    if len(rawResponse) > 0:
        faceRectangle = rawResponse[0]['faceRectangle']
        emotionList = rawResponse[0]['faceAttributes']['emotion']
        emotion = max(emotionList.items(), key=operator.itemgetter(1))[0]

        formattedRes = {}
        formattedRes['faceRectangle'] = faceRectangle
        formattedRes['emotion'] = emotion
        return jsonify(formattedRes)
    else:
        return jsonify({"Error": "COULD_N0T_DETECT_FACE"}) 

if __name__ == '__main__':
	app.run()