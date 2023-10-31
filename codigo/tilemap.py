NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'}
import pygame
import json


class Tilemap:
    def __init__(self, jogo, tile_size=16):
        self.jogo = jogo
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile)
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    def tiles_around(self, pos):
        tiles = []
        tiles_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tiles_loc[0] + offset[0]) + ';' + str(tiles_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)

    def load(self, path):
        with open(path, 'r') as f:
            map_data = json.load(f)
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def remove_tile(self, pos):
        tile_loc = str(pos[0]) + ';' + str(pos[1])
        if tile_loc in self.tilemap:
            del self.tilemap[tile_loc]
        for tile in self.offgrid_tiles.copy():
            if tile['pos'] == pos:
                self.offgrid_tiles.remove(tile)

    def remove_parede(self, pos):
        tile_loc = str(pos[0]) + ';' + str(pos[1])
        if tile_loc in self.tilemap:
            del self.tilemap[tile_loc]
        for tile in self.offgrid_tiles.copy():
            if tile['pos'] == pos:
                self.offgrid_tiles.remove(tile)

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.jogo.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        for x in range(int(offset[0]) // int(self.tile_size), (int(offset[0]) + surf.get_width()) // int(self.tile_size) + 1):
            for y in range(int(offset[1]) // int(self.tile_size), (int(offset[1]) + int(surf.get_height())) // int(self.tile_size + 1)):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.jogo.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))