# Album of the Week
Review music albums with friends.

## How it Works
Each week a new album is promoted to be the Album of the Week (AOTW). Users share their thoughts and rate the album on a -5 to +5 scale. Meanwhile, users search for albums to nominate for the next AOTW. Group admins finalize the AOTW by selecting from user nominations. 

## Searching the Database
This app relies on the AudioDB database (https://www.theaudiodb.com/) for artist and album name results. The app makes an API call to the AudioDB and displays results to the user. While this database is extensive, it is not exhaustive. If an album does not exist in the database, users have the option to add the album manually. These albums are stored in a PostgreSQL database. 

All searches query both the local and external databases, displaying all results to the user. Duplicates are eliminated. 

## Django Models
The app stores user, album, nomination, and review data in a PostgreSQL database. Once an album has been nominated for AOTW, an album object is created and the app will no longer query the external AudioDB database for the album's information. 

## Future Features
- Linking albums to Spotify API so users can click and listen to the AOTW
- Remove django-avatar package and rely on Cloudinary for profile image manipulation
- Allow users to add reviews to past AOTW's
- Allow users to edit/change their saved reviews

## Design
This app uses a mobile-first responsive design. Materialize CSS was used for the front-end. This framework allows easy manipulation of the grid for responsive design. Some JavaScript was used to improve the UX. 


