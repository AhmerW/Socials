from common.data.local.queries.query import QueryCreator


class NoticeQ(metaclass=QueryCreator):
    GET_WHERE_AUTHOR_AND_TARGET = \
        """
        SELECT * from notices WHERE notice_author = {author} AND notice_target = {target};
        """

    GET_WHERE_TARGET = \
        """
        SELECT * FROM notices WHERE notice_target = {target} OFFSET {offset} LIMIT {limit};
        """

    DELETE_WHERE_AUTHOR_AND_TARGET =\
        """
        DELETE FROM notices WHERE notice_author = {author} and notice_target = {target};
        """

    INSERT = \
        """
        INSERT INTO 
            notices(
                notice_author,
                notice_target,
                notice_event,
                notice_title,
                notice_body,
                notice_data
            )
            
            VALUES (
                {author},
                {target},
                {event},
                {title},
                {body},
                {data}
            )
        """
