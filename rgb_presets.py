from pathlib import Path

import json
import subprocess

import aura
import led_sync
import keyboard
import paths

def parse_color(color):
  if type(color) == list and len(color) == 1:
    color = color[0]
  elif type(color) == list and len(color) == 3:
    color = ','.join(color)

  assert type(color) == str and color.count(',') == 2
  
  return color

def set_rgb(**kwargs):
  primary = kwargs.get('primary')
  accent = kwargs.get('accent')

  # call rgb updates
  aura.update_aura(kwargs.get('aura_mode'), primary)
  led_sync.update_LED_Sync(kwargs.get('led_sync_mode'), primary, accent, kwargs.get('led_sync_speed'))
  keyboard.update_kb(primary, accent)
  cam = f"python {paths.COLCTL} -m {kwargs.get('cam_mode')} -as {kwargs.get('cam_speed')} "
  if primary:
    cam += f"-c0 {primary} -c1 {accent} -cc 2 -c {primary} "
  subprocess.call(cam)

  # save profile for cam startup
  cam += '--fan_speed "(20,25),(30,60),(40,90),(45,100)" ' \
    '--pump_speed "(20,60),(50,100)" '
  with open('CAM Startup.bat', 'w') as f:
    f.write(cam)


def update_rgb(preset_name):
  with open(f'{paths.CURR_DIR}\\presets.json', 'r') as f:
    presets = json.load(f)
    
  if preset_name in presets:
    set_rgb(**{**presets['default_values'], **presets.get(preset_name)})
  else:
    presets_list = ''
    for p in presets.keys():
      if p != 'default_values':
        presets_list += '\n\t' + p
    
    print(f'No preset for {preset_name}, must be one of:{presets_list}')


if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('-p', '--preset', help='RGB preset')
  parser.add_argument('-pc', '--primary', nargs='+', help='RGB primary color as R,G,B or R G B')
  parser.add_argument('-ac', '--accent', nargs='+', help='RGB accent color as R,G,B or R G B')
  parser.add_argument('-am', '--aura_mode', nargs='+', help='ASUS AURA lighting mode')
  parser.add_argument('-cm', '--cam_mode', nargs='+', help='NZXT CAM lighting mode')
  parser.add_argument('-lm', '--led_sync_mode', nargs='+', help='EVGA LED Sync lighting mode')
  parser.add_argument('-cs', '--cam_speed', nargs='+', help='NZXT CAM lighting animation speed')
  parser.add_argument('-ls', '--led_sync_speed', nargs='+', help='EVGA LED Sync lighting animation speed')
  args = parser.parse_args()

  with open(f'{paths.CURR_DIR}\\presets.json', 'r') as f:
    presets = json.load(f)

  if args.preset:
    if args.preset in presets:
      set_rgb(**{**presets['default_values'], **presets.get(args.preset)})
    else:
      presets_list = ''
      for p in presets.keys():
        if p != 'default_values':
          presets_list += '\n\t' + p
      
      print(f'No preset for {args.preset}, must be one of:{presets_list}')
  else:
    set_rgb(**{**presets['default_values'], **args})