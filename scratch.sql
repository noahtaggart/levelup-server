    SELECT
            u.id as user_id,
            u.first_name,
            u.last_name,
            g.*
            
            
            from auth_user u
            join levelupAPI_gamer gr ON u.id = gr.user_id
            join  levelupAPI_game g ON gr.id = g.gamer_id


            SELECT
                    e.*,
                    g.title as "Game Title",
                    u.first_name || " " || u.last_name AS full_name
                FROM levelupapi_event e
                JOIN levelupapi_gamer gr
                    ON gr.id = e.organizer_id
                JOIN auth_user u
                    ON u.id = gr.id
                JOIN levelupapi_game g
                    ON g.id = e.game_id

CREATE VIEW GAMES_BY_USER1 AS
SELECT
    g.*,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN
    levelupapi_gamer gr ON g.gamer_id = gr.id
JOIN
    auth_user u ON gr.user_id = u.id
;

CREATE VIEW EVENTS_BY_USER AS
SELECT
    e.*,
    g.title,
    u.first_name || " " || u.last_name AS full_name
    FROM levelupapi_event e
    JOIN levelupapi_gamer gr
        ON gr.id = e.organizer_id
    JOIN auth_user u
        ON u.id = gr.id
    JOIN levelupapi_game g
        ON g.id = e.game_id