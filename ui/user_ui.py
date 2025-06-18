def add_usage_message():
    return "Usage: !role add <username> <role>"

def role_altered_message(user):
    return f"Role: altered for '{user.user_name}' to '{user.user_role}'."

def list_user_message(users):
    return "list of users:\n" + "\n".join(
        f"[{u.user_name}] {u.user_role}"
        for u in users
    ) 

def no_user_message():
    return "uhoh there seems to be no users updating user list"

def permission_too_low_message(name):
    return f"please check permissions level \"{name}\" does not have correct permissions to use this command"

def user_added_message(user):
    return f"user: '{user.user_name}' has been added with role: '{user.user_role}'."

def user_not_found_message(name):
    return f"user: {name} is not a member within the discord network please try a different name or run the \"!user list\" command"

def user_already_on_list(name):
    return f"user: {name.user_name} is already on the list of users as {name.user_role} "

def alter_usage_message():
    return "Usage: !role alter <username> <\"student|teacher\">"

def usage_message():
    return f"Usage: !user [add|list|alter] ..."