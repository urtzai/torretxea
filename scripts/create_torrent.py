import delegator
import os
import glob
import errno
import pdb
import time

# FILM PATHS
FILM_PATH_TO_SHARE = ''
FILM_PATH_MEDIA_STORE = ''

# SERIE PATHS
SERIES_PATH_TO_SHARE = ''
SERIES_PATH_MEDIA_STORE = ''

# CONFIGURATION
TORRENT_STORE_PATH = ''
TRANSMISSION_AUTH = ""
COMMENT = "TORRETXEAK eskainitako euskarazko media"

def main():
    # START CREATING FILM TORRENTS
    files = glob.glob(FILM_PATH_TO_SHARE + '*')
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
                MKDIR_MEDIA_STORE = delegator.run("mkdir -p {0}".format(media_store_path), block=True)
                # process = subprocess.Popen(MKDIR_MEDIA_STORE.split(), stdout=subprocess.PIPE)
                
                # MOVE MEDIA TO STORE FOLDER
                MV_MEDIA_STORE = delegator.run('mv {0} {1}'.format(f.name, media_store_path), block=True)
                # process = subprocess.Popen(MV_MEDIA_STORE.split(), stdout=subprocess.PIPE)

                # CREATE TORRENT FILE
                file_name_ext = "%s.%s" % (file_name, file_ext)
                media_store_file_path = os.path.join(media_store_path, file_name_ext)
                torrent_file_path = os.path.join(TORRENT_STORE_PATH, file_name_ext)
                CREATE_TORRENT_CMD = delegator.run('transmission-create -o {0}.torrent -c {1} -t udp://tracker.openbittorrent.com:80 -t udp://open.demonii.com:1337 -t udp://tracker.coppersurfer.tk:6969 -t udp://tracker.leechers-paradise.org:6969 {2}'.format(torrent_file_path, COMMENT, media_store_file_path), block=True) #TODO: Trackerrak aparteko fitxategi edo datu iturri batetik (zerrenda batetik) hartzea komeni da
                # process = subprocess.Popen(CREATE_TORRENT_CMD.split(), stdout=subprocess.PIPE)

                # SHARE TORRENT
                SHARE_TORRENT_CMD = delegator.run('transmission-remote --auth={0} --add {1}'.format(TRANSMISSION_AUTH, torrent_file_path), block=True)
                # process = subprocess.Popen(SHARE_TORRENT_CMD.split(), stdout=subprocess.PIPE)
        except IOError as exc:
            print "ERROREA: Fitxategiak irakurtzean"

if __name__ == "__main__": 
    main()
