# ytdl-web
A web interface for the `youtube_dl` Python library
## `/`
User Interface: easily paste a link or ID and see all available formats (and codec info), preview formats, and view download links and embed code.
## `/api`
`youtube_dl` API  
`GET`: Provide a link or id as the `v` search parameter  
`POST`: Provide a json object containing the link or id in the key `identifier`  
## `/watch`
Redirect to the source content, can be used for embedding videos in pages  
`GET`: Provide a link or id as the `v` search parameter, and the format index as the `fmt` search parameter  
The user interface can generate this url (with fmt index) for you.  
The `fmt` parameter is optional. If not provided, the highest available quality (last index) video+audio format will be selected.