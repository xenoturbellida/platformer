level_map = [
    '      XXX               ',
    '          1 X           ',
    'X X X     XXX X         ',
    'X X X 2  XXXXXX         ',
    'XXXXXXXXXXXXXXX         ',
    'XXXXXX  XXXXXXX         ',
    'XXXXXXXXXXXXXXXXXXXXXXXX',
    'XX  XXXXXXXXXXX         ',
    'XXXXXXXXXXXXXXX         ',
    'XXXXXXXXXXXXXXX         ',
    'XXXXXXXXXXXXXXX         '
]

tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size
fps = 60
start_position_player_1 = (10*tile_size, 2*tile_size)
start_position_player_2 = (7*tile_size, 4*tile_size)
