from pyfirebasehandler.firebase_handler import FirebaseHandler

handler = FirebaseHandler('frag-abi-firebase-adminsdk-omiht-47fc996ced.json')


def get_user_data(user_id):
    return handler.get_document("users", user_id)
