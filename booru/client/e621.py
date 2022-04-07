import requests
import json
import re
from ..utils.parser import Api, better_object, parse_image, get_hostname
from random import shuffle, randint

Booru = Api()


class E621(object):
    """e621 wrapper

    Methods
    -------
    search : function
        Search and gets images from e621.

    get_image : function
        Gets images, meant just image urls from e621.

    """

    @staticmethod
    def append_obj(raw_object: dict):
        """Extends new object to the raw dict

        Parameters
        ----------
        raw_object : dict
            The raw object returned by e621.

        Returns
        -------
        str
            The new value of the raw object
        """
        for i in range(len(raw_object)):
            if "id" in raw_object[i]:
                raw_object[i][
                    "post_url"
                ] = f"{get_hostname(Booru.e621)}/posts/{raw_object[i]['id']}"

        return raw_object

    def __init__(self, api_key: str = "", user_id: str = ""):
        """Initializes e621.

        Parameters
        ----------
        api_key : str
            Your API Key which is accessible within your account options page

        user_id : str
            Your user ID, which is accessible on the account options/profile page.
        """

        if api_key and user_id == "":
            self.api_key = None
            self.user_id = None
        else:
            self.api_key = api_key
            self.user_id = user_id

        self.specs = {"api_key": self.api_key, "user_id": self.user_id}

    async def search(
        self,
        query: str,
        block: str = "",
        limit: int = 100,
        page: int = 1,
        random: bool = True,
        gacha: bool = False,
    ):

        """Search and gets images from e621.

        Parameters
        ----------
        query : str
            The query to search for.

        block : str
            The disgusting query you want to block

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        random : bool
            Shuffle the whole dict, default is True.

        gacha : bool
            Get random single object, limit property will be ignored.

        Returns
        -------
        dict
            The json object returned by e621.
        """
        if gacha:
            limit = 100

        if limit > 100:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        if block != "":
            self.query = f"{query} -{block}*"

        else:
            self.query = query

        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["page"] = str(page)

        self.data = requests.get(Booru.e621, params=self.specs, headers=Booru.headers)
        self.final = json.loads(better_object(self.data.json()), encoding="utf-8")

        if not self.final["posts"]:
            raise ValueError(Booru.error_handling_null)

        self.not_random = E621.append_obj(self.final["posts"])
        shuffle(self.not_random)

        try:
            if gacha:
                return better_object(self.not_random[randint(0, len(self.not_random))])

            elif random:
                return better_object(self.not_random)

            else:
                return better_object(E621.append_obj(self.final["posts"]))

        except Exception as e:
            raise ValueError(f"Failed to get data: {e}")

    async def get_image(
        self, query: str, block: str = "", limit: int = 100, page: int = 1
    ):

        """Gets images, meant just image urls from e621.

        Parameters
        ----------
        query : str
            The query to search for.

        block : str
            The disgusting query you want to block

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        Returns
        -------
        list
            The list of image urls.

        """

        if limit > 100:
            raise ValueError(Booru.error_handling_limit)

        if block and re.findall(block, query):
            raise ValueError(Booru.error_handling_sameval)

        if block != "":
            self.query = f"{query} -{block}*"

        else:
            self.query = query

        self.specs["tags"] = str(self.query)
        self.specs["limit"] = str(limit)
        self.specs["pid"] = str(page)
        self.specs["json"] = "1"

        try:
            self.data = requests.get(
                Booru.e621, params=self.specs, headers=Booru.headers
            )
            self.final = json.loads(better_object(self.data.json()), encoding="utf-8")

            self.not_random = parse_image(self.final["posts"])
            shuffle(self.not_random)
            return better_object(self.not_random)

        except:
            raise ValueError(f"Failed to get data")
