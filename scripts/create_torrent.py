import yaml
import delegator
import os
import glob
import errno
import time


try:
    with open("conf.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    FILM_PATH_TO_SHARE = cfg.get('paths').get('FILM_PATH_TO_SHARE')
    FILM_PATH_MEDIA_STORE = cfg.get('paths').get('FILM_PATH_MEDIA_STORE')
    SERIES_PATH_TO_SHARE = cfg.get('paths').get('SERIES_PATH_TO_SHARE')
    SERIES_PATH_MEDIA_STORE = cfg.get('paths').get('SERIES_PATH_MEDIA_STORE')
    TORRENT_STORE_PATH = cfg.get('transmission').get('TORRENT_STORE_PATH')
    TRANSMISSION_AUTH = cfg.get('transmission').get('TRANSMISSION_AUTH')
    COMMENT = cfg.get('transmission').get('COMMENT')

except IOError as exc:
    print "Can't load config file"


def create_media_store_folders(media_store_path):
    command = delegator.run("mkdir -p {0}".format(media_store_path), block=True)
    print command.out


def move_file_to_media_store(f, media_store_path):
    command = delegator.run('mv {0} {1}'.format(f.name, media_store_path), block=True)
    print command.out


def create_torrent_file(file_name, file_name_ext, media_store_path):
    media_store_file_path = os.path.join(media_store_path, file_name_ext)
    torrent_name = "%s.torrent" % file_name
    torrent_file_path = os.path.join(TORRENT_STORE_PATH, torrent_name)
    command = delegator.run('transmission-create -o {0} -c {1} -t udp://tracker.openbittorrent.com:80 -t udp://open.demonii.com:1337 -t udp://tracker.coppersurfer.tk:6969 -t udp://tracker.leechers-paradise.org:6969 {2}'.format(torrent_file_path, COMMENT, media_store_file_path), block=True) #TODO: Trackerrak aparteko fitxategi edo datu iturri batetik (zerrenda batetik) hartzea komeni da
    print command.out
    return torrent_file_path


def share_torrent_file(torrent_file_path):
    command = delegator.run('transmission-remote --auth={0} --add {1}'.format(TRANSMISSION_AUTH, torrent_file_path), block=True)
    print command.out


def process_files(process_path):
    # START READING TO SHARE FILES
    files = glob.glob(process_path + '*')
    for name in files:
        try:
            with open(name) as f:
                file_name, file_ext = os.path.basename(f.name).split(".")
                folder_names = file_name.split("_")

                # CREATE FOLDER PATHS
                media_root = folder_names[0].upper()
                if len(folder_names) > 2:
                    season_name = folder_names[1][0:3].upper()
                    media_relative_path = os.path.join(media_root, season_name)
                else:
                    media_relative_path = media_root
                media_store_path = os.path.join(FILM_PATH_MEDIA_STORE, media_relative_path)
                
                # CREATE MEDIA STORE FOLDERS
                create_media_store_folders(media_store_path)

                # MOVE MEDIA TO STORE FOLDER
                move_file_to_media_store(f, media_store_path)

                # CREATE TORRENT FILE
                file_name_ext = "%s.%s" % (file_name, file_ext)
                torrent_file_path = create_torrent_file(file_name, file_name_ext, media_store_path)

                # SHARE TORRENT
                share_torrent_file(torrent_file_path)
                
        except IOError as exc:
            print "ERROREA: Fitxategiak irakurtzean"



if __name__ == "__main__": 
    process_files(FILM_PATH_TO_SHARE)
    process_files(SERIES_PATH_TO_SHARE)
