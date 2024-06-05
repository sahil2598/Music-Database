# Music Database Management System

## Overview

The Music Database Management System (MDMS) is designed to store and manage information related to songs, artists, albums, record labels, genres, and streaming platforms. It provides functionalities to add, remove, update, and query data efficiently, ensuring robust management of musical entities and their relationships.

## Features

- Manage songs with details such as track name, duration, and number of streams.
- Organize albums, linking them to specific artists and containing multiple songs.
- Store artist information including name, date of birth, and nationality.
- Handle record label data including name, address, and phone number.
- Categorize songs by genres and manage genre information.
- Track streaming platforms, their subscription fees, and total subscribers.
- Ensure robust relationships between songs, artists, albums, labels, genres, and streaming platforms.

## Entity Relationships

### Songs
- **Identified by:** `TrackID`
- **Attributes:** `trackName`, `duration`, `NumberOfStreams`
- **Relationships:**
  - Belongs to one album
  - Composed by multiple artists
  - Produced by multiple record labels
  - Belongs to a single genre
  - Streamed on multiple platforms

### Artists
- **Identified by:** `ArtistID`
- **Attributes:** `ArtistName`, `DOB`, `Nationality`
- **Relationships:**
  - Can compose multiple songs
  - Each album is associated with one artist

### Albums
- **Identified by:** `AlbumID`
- **Attributes:** `AlbumName`, `ReleaseDate`
- **Relationships:**
  - Contains multiple songs
  - Associated with one artist

### Record Labels
- **Identified by:** `LabelID`
- **Attributes:** `LabelName`, `Address`, `PhoneNumber`
- **Relationships:**
  - Can produce multiple songs for multiple artists

### Genres
- **Identified by:** `GenreID`
- **Attributes:** `genreName`, `origin`
- **Relationships:**
  - Can have many songs

### Streaming Platforms
- **Identified by:** `PlatformID`
- **Attributes:** `PlatformName`, `SubscriptionFee`, `TotalSubscribers`
- **Relationships:**
  - Can stream multiple songs

## Execution
```bash
python music_database.py
```