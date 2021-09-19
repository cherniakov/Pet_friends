import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self,
                    email: str,
                    password: str) -> json:
        """
        Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        с уникальным ключем пользователя, найденного по указанному email и паролю
        """
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """
        Метод делает запрос к API сервера и возвращает статус запроса
        и результат в формате JSON со списком найденных питомцев, совподающих с фильтром.
        На данный момент с фильтром пустое значение - получит список всех питомцев,
        либо "my_pets" - получит список питомцев пользователя.
        """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_pet(self, auth_key: json,
                      name: str,
                      animal_type: str,
                      age: str,
                      pet_photo: str) -> json:
        """
        Метод делает запрос к API сервера и добавляет инфомацию о новом питомце на сервер.
        Возвращает статус запроса и результат со добавленном питомце в формате JSON.
        """

        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: int) -> json:

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + str(pet_id), headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_pet(self, auth_key: json,
                 pet_id: str,
                 name: str,
                 animal_type: str,
                 age: int,) -> json:
        headers = {'auth_key': auth_key['key']}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age,
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_creat_pet(self, auth_key: json,
                        name: str,
                        animal_type: str,
                        age: int) -> json:
        """
        Метод делает запрос к API сервера и создает нового питомца на сервер.
        Возвращает статус запроса и результат со добавленном питомце в формате JSON.
        """

        headers = {'auth_key': auth_key['key']}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age,
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

