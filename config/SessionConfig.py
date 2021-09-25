import threading


class SessionConfig:

    def __init__(self):
        self.param_set = self.init_param_set()
        self.message_dict, self.message_texts = self.init_message_dict()

    def init_param_set(self):
        param_set = set()
        param_set.add("currency")
        param_set.add("curr.new")
        param_set.add("curr.old")
        param_set.add("product")
        param_set.add("quantity")
        param_set.add("id")
        return param_set

    def init_message_dict(self):
        message_dict = {}
        message_dict["home"] = 0
        message_dict["setting currency"] = 1
        message_dict["serving product page"] = 2
        message_dict["view user cart"] = 3
        message_dict["adding to cart"] = 4
        message_dict["placing order"] = 5
        message_dict["order placed"] = 5
        message_texts = ["home", "setting currency", "serving product page",
                         "view user cart", "adding to cart", "checkout"]
        return message_dict, message_texts

session_config = SessionConfig()