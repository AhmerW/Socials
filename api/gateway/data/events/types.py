# System Events
# update -> PATCH (in rest conventions)
system_events = {
    "db.init.start",
    "db.init.done",
    "user.profile.update",
    "chat.message.post",
    "chat.message.delete",
    "chat.message.update",
    "chat.profile.update",
    "friend.request.post",
    "friend.request.delete",
    "post.like.post",
    "post.like.delete",
    "post.comment.post",
    "post.comment.delete",
    "post.comment.like.post",
    "post.comment.like.delete",
}


def updateToPatch(event: str):
    # update can only be the last topic
    return ".".join(
        [
            *event.split(".")[0:-2],
            "patch",
        ],
    )
