import asyncio
import aiohttp
import ujson
import logging
import base64

logger = logging.getLogger(__name__)

class Text2Image:
    def __init__(self, api_key, secret_key):
        self._headers = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }
        self._session: Optional[aiohttp.ClientSession] = None
        self._model_id = None

    async def _get_model_id(self):
        async with self._session.get('/key/api/v1/models', headers=self._headers) as response:
            if response.status != 200:
                raise Exception('unable to get text2image model id')
            data = await response.json()
            return data[0]['id']

    async def _post_generate(self, prompt, images, width, height):
        params = {
            'type': 'GENERATE',
            'numImages': images,
            'width': width,
            'height': height,
            'generateParams': {
                'query': f'{prompt}'
            }
        }

        files = aiohttp.FormData()
        files.add_field(name='model_id', value=f'{self._model_id}')
        files.add_field(name='params', value=ujson.dumps(params), content_type='application/json')

        async with self._session.post('/key/api/v1/text2image/run', headers=self._headers, data=files) as response:
            if response.status != 200 and response.status != 201:
                raise Exception(f'unable to post task (response-code = {response.status})')
            data = await response.json()
            return data['uuid']

    async def _check_generation(self, uuid):
        async with self._session.get(f'/key/api/v1/text2image/status/{uuid}', headers=self._headers) as response:
            if response.status != 200 and response.status != 201:
                raise Exception(f'unable to get status (uuid = {uuid})')
            return await response.json()


    async def generate(self, prompt, images=1, width=1024, height=1024):
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession('https://api-key.fusionbrain.ai')
        if not self._model_id:
            self._model_id = await self._get_model_id()
        uuid = await self._post_generate(prompt, images, width, height)

        attempts = 10
        delay = 10

        while attempts > 0:
            data = await self._check_generation(uuid)
            logging.info(f'generation status uuid={uuid} status={data['status']}')
            if data['status'] == 'DONE':
                break
            attempts -= 1
            await asyncio.sleep(delay)

        if data['status'] != 'DONE':
            logging.warning(f'{data}')
            raise Exception('failed to generate image')

        return [ base64.b64decode(image) for image in data["images"] ]

