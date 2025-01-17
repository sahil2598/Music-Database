CREATE TABLE IF NOT EXISTS Artists (
    ArtistID INTEGER PRIMARY KEY AUTO_INCREMENT,
    ArtistName VARCHAR(255) NOT NULL,
    DOB DATE,
    Nationality VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Albums (
    AlbumID INTEGER PRIMARY KEY AUTO_INCREMENT,
    ArtistID INTEGER NOT NULL,
    AlbumName VARCHAR(255) NOT NULL,
    ReleaseDate DATE,
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
);

CREATE TABLE IF NOT EXISTS Genres (
    GenreID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Origin VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS RecordLabels (
    LabelID INTEGER PRIMARY KEY AUTO_INCREMENT,
    LabelName VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(255),
    Address TEXT
);

CREATE TABLE IF NOT EXISTS Songs (
    TrackID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Duration INT,
    TrackName VARCHAR(255) NOT NULL,
    GenreID INTEGER,
    LabelID INTEGER,
    AlbumID INTEGER,
    ArtistID INTEGER,
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID),
    FOREIGN KEY (LabelID) REFERENCES RecordLabels(LabelID),
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID),
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
);

CREATE TABLE IF NOT EXISTS Compose (
    ArtistID INTEGER,
    TrackID INTEGER,
    PRIMARY KEY (ArtistID, TrackID),
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID),
    FOREIGN KEY (TrackID) REFERENCES Songs(TrackID)
);

CREATE TABLE IF NOT EXISTS StreamingPlatforms (
    PlatformID INTEGER PRIMARY KEY AUTO_INCREMENT,
    PlatformName VARCHAR(255) NOT NULL,
    TotalSubscribers INT,
    SubscriptionFee DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Streams (
    PlatformID INTEGER,
    TrackID INTEGER,
    NumberOfStreams INT,
    PRIMARY KEY (PlatformID, TrackID),
    FOREIGN KEY (PlatformID) REFERENCES StreamingPlatforms(PlatformID),
    FOREIGN KEY (TrackID) REFERENCES Songs(TrackID)
);


