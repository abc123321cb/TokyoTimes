"""Player configuration - hitbox, speed, and other player-specific tuning."""

# Sprite dimensions and scaling
SPRITE_FRAME_WIDTH = 290  # Original frame width
SPRITE_FRAME_HEIGHT = 440  # Original frame height
PLAYER_SPRITE_SCALE = 0.5  # Scale sprite to 50%

# Computed scaled dimensions
SCALED_SPRITE_WIDTH = int(SPRITE_FRAME_WIDTH * PLAYER_SPRITE_SCALE)
SCALED_SPRITE_HEIGHT = int(SPRITE_FRAME_HEIGHT * PLAYER_SPRITE_SCALE)

# Player hitbox configuration (defined in ORIGINAL sprite coordinates)
# These values are based on the 290x440 unscaled sprite and will be scaled automatically
# This is the collision box at the player's feet
PLAYER_HITBOX_WIDTH_UNSCALED = 150
PLAYER_HITBOX_HEIGHT_UNSCALED = 50

# Offsets from sprite origin (top-left) to position the hitbox at the feet
# These are in ORIGINAL sprite coordinates (290x440) and will be scaled automatically
PLAYER_HITBOX_OFFSET_CENTERX_UNSCALED = 150  # horizontal offset to feet center
PLAYER_HITBOX_OFFSET_BOTTOM_UNSCALED = 420  # vertical offset to feet bottom

# Computed scaled values (DO NOT EDIT - these are calculated automatically)
PLAYER_HITBOX_WIDTH = int(PLAYER_HITBOX_WIDTH_UNSCALED * PLAYER_SPRITE_SCALE)
PLAYER_HITBOX_HEIGHT = int(PLAYER_HITBOX_HEIGHT_UNSCALED * PLAYER_SPRITE_SCALE)
PLAYER_HITBOX_OFFSET_CENTERX = int(PLAYER_HITBOX_OFFSET_CENTERX_UNSCALED * PLAYER_SPRITE_SCALE)
PLAYER_HITBOX_OFFSET_BOTTOM = int(PLAYER_HITBOX_OFFSET_BOTTOM_UNSCALED * PLAYER_SPRITE_SCALE)

# Movement
PLAYER_SPEED = 300
