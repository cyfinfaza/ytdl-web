# ytdl-web
a web interface for the `youtube_dl` Python library
## `/`
user interface
## `/api`
youtube_dl api  
`GET`: provide a link or id as the `v` search parameter  
`POST`: provide a json object containing the link or id in the key `identifier`  
## `/watch`
redirect to the highest available quality video+audio source  
`GET`: provide a link or id as the `v` search parameter  