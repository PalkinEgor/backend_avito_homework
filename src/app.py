from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
from plate_reader_client import PlateReaderClient
import logging
import io

app = Flask(__name__)
plate_reader_model = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')
client = PlateReaderClient('http://89.169.157.72:8080')


@app.route('/')
def hello():
    return '<h1><center>Hello!</center></h1>'


def image_processor(image_id):
    try:
        image = io.BytesIO(client.read_image(image_id))
    except Exception as e:
        return {'error': str(e)}, 400
    
    try:
        return plate_reader_model.read_text(image), 200
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/plate_reader/<image_id>', methods=['GET'])
def plate_reader_one(image_id):
    return image_processor(image_id)  


@app.route('/plate_reader', methods=['GET'])
def plate_reader_many():
    image_ids = request.args.get('image_ids')
    if not image_ids:
        return {'error': 'No image_ids provided'}, 400
    image_ids = image_ids.split(',')
    
    result = {}
    for image_id in image_ids:
        current_result, code = image_processor(image_id)
        if code == 200:
           result[image_id] = current_result
        else:
            result[image_id] = current_result['error']
    return result


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.run(host='0.0.0.0', port=8080, debug=True)
