## API Tomkits Documentation

### **POST**  -  **Register**

-   **Endpoint:**  
    `POST http://34.50.72.127/auth/register`
    
-   **Description:**  
    This endpoint is used to register a new user into the system. Users must provide data such as username, email, and password. If the registration is successful, the system will create a new account for the user.

**Request Parameters:**
- username (string): The username to be used for login or identification.
- email (string): A valid email address for communication or password recovery purposes.
- password (string): A password to be used for login.

**Request Body:**
```json
{
  "username": "Umam ganteng",
  "email": "umamgantengea@gmail.com",
  "password": "ammanazza"
}
```
**Responses:**

-   **201 Created**  
    Success:
	```json
	{ "message": "User registered successfully." }
	```
- **409 Conflict**  
Error (User already exists):
	```json
	{ "error": "User already exists" }
	```

### **POST**  -  **User Login**

-   **Endpoint:**  
    `POST http://34.50.72.127/auth/login`
    
-   **Description:**  
    This endpoint is used to authenticate users who are already registered in the system. Users must provide a valid email and password to gain access to the services.

**Request Parameters:**
- email (string): email (string): The email address used during registration.
- password (string): The password associated with the account.


**Request Body:**
```json
{
  "email": "umamgantengea@gmail.com",
  "password": "ammanazza"
}
```
**Responses:**

-   **200 OK**  
    Success (Login successful):
    ```json 
    { "message": "You are logged in.", 
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
      ```
- **400 Bad Request**  
Error (Invalid email or password):
	```json
	{ "error": "Invalid email or password." }
	```

### **GET**  -  **User Identity (WhoAmI)**

-   **Endpoint:**  
    `GET http://34.50.72.127/auth/whoami`
    
-   **Description:**  
    This endpoint retrieves information about the currently logged-in user based on the authentication token (JWT). It is useful for verifying user identity or displaying profile information.

**Responses:**

-   **200 OK**  
    Success:
    ```json
	{
	  "user_id": "<unique_user_id>",
	  "username": "Paulus Aditya Wicaksono",
	  "email": "paulusaditya22@gmail.com",
	}

    ```
    **Authorization:**  
Bearer Token  
`<token>`

### **POST**  -  **Refresh Access Token**

**Endpoint:**  
`POST http://34.50.72.127/auth/refresh`

**Description:**  
This endpoint is used to renew or obtain a new access token (JWT) using a valid refresh token. It is helpful if the previous access token has expired but the refresh token is still active.


**Responses:**

-   **200 OK**  
    Success:
    ```json
      {  
      "new_accesstoken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." 
      }
      ```
**Authorization:**  
Bearer Token  
`<token>`

### **POST**  -  **User Logout**

**Endpoint:**  
`POST http://34.50.72.127/auth/logout`

**Description:**  
This endpoint logs out the user by invalidating the authentication token, both access and refresh tokens.
**Responses:**

-   **200 OK**  
    Success:
    ```json
        {  
        "message":  "access token revoked successfully"
        }
       ```
**Authorization:**  
Bearer Token  
`<token>`

### **POST**  -  **Predict Disease**

**Endpoint:**  
`POST http://34.50.72.127/predict/disease`

**Description:**  
This endpoint predicts plant diseases based on the uploaded image. The system uses a machine learning model to analyze the image and return a disease prediction.

**Request:**

-   **Headers:**  
    `Content-Type: multipart/form-data`  
    `Authorization: Bearer <token>`
    
-   **Body (form-data):**  
    `file: <image-file>`
    

**Responses:**

-   **400 Bad Request**  - No file uploaded
    ```json
    { "Response Text": "Invalid File Format." }
    ```
 - **400 Bad Request** - Invalid file format
     ```json
    { "Response Text": "Invalid File Format." }
    ```
  - **400 Bad Request** - Not a valid tomato leaf
       ```json
    { "Response Text": "Bukan daun tomat." }
    ```
   - **401 Unauthorized** - Expired or invalid token
	 ```json
	 { "Response Text": "Token has expired ." }
	 ```
-  **200 OK** - Prediction successful
	 ```json
	    {
	    "confidence": "98.74%",
	    "deskripsi": "Leaf mold is caused by the fungus Passalora fulva, and it affects the leaves, causing them to turn yellow and become moldy.",
	    "nama_penyakit": "Leaf_Mold",
	    "rekomendasi_product": [
	        {
	            "active_ingredient": "Propamocarb Hydrochloride",
	            "product_image": "https://storage.googleapis.com/tomkits/product/Previcur.png",
	            "product_name": "Previcur Flex"
	        },
	        {
	            "active_ingredient": "Chlorothalonil",
	            "product_image": "https://storage.googleapis.com/tomkits/product/Daconil_Fungicide.png",
	            "product_name": "Daconil Fungicide"
	        },
	        {
	            "active_ingredient": "Bacillus subtilis",
	            "product_image": "https://storage.googleapis.com/tomkits/product/Serenade_Garden.png",
	            "product_name": "Serenade Garden"
	        }
	    ],
	    "solusi": "Improve air circulation around the plants, prune affected leaves, and apply fungicides like azoxystrobin."
	    }
	 ```
### **POST**  -  **Predict Tomato**

**Endpoint:**  
`POST http://34.50.72.127/predict/tomato`

**Description:**  
This endpoint is used to predict the quality and type of a tomato based on an uploaded image. The system uses a machine learning model to analyze the image of the tomato and classify it into categories such as ripeness and type (e.g., variety of tomato). The predictions provide confidence scores for the respective classifications.

**Request:**

-   **Headers:**  
    `Content-Type: multipart/form-data`  
    `Authorization: Bearer <token>`
    
-   **Body (form-data):**  
    `file: <image-file>`
**Responses:**

-   **400 Bad Request**  - No file uploaded
    ```json
    { "Response Text": "Invalid File Format." }
    ```
- **400 Bad Request** - Invalid file format
     ```json
    { "Response Text": "Invalid File Format." }
    ```
- **401 Unauthorized** - Expired or invalid token
	 ```json
	{
	"error": "invalid_token",
	"message": "Signature verification failed"
	}
	```
-  **200 OK** - Prediction successful
	 ```json
	{
	    "Quality": {
	        "Class": "Ripe",
	        "Confidence": 96.78627848625183
	    },
	    "Type": {
	        "Class": "cherokee_purple",
	        "Confidence": 49.00272488594055
	    }
	}
	 ```


### **GET**  -  **Prediction History**

**Endpoint:**  
`GET http://34.50.72.127/predict/history`

**Description:**  
This endpoint retrieves the history of disease predictions for the currently logged-in user.
**Responses:**

-   **200 OK**  
    Success:
    ```json
			{

			"histories":  [

			{"disease_name":  "Leaf_Mold",

			"id":  "0cddea8a-0a4d-417c-b7d4-a9a6e27005a5",

			"image_link":  "https://storage.googleapis.com/tomkits/images/1e82a7f3-165d-4e56-8233-e2fc80a0e059.jpg"},

			{

			"disease_name":  "Leaf_Mold",

			"id":  "4869eed9-b452-4ae2-8b76-77bc557d860d",

			"image_link":  "https://storage.googleapis.com/tomkits/images/2602d5b2-ec3d-4b01-947e-70c7d790cddb.jpg"},

			{

			"disease_name":  "Bacterial_Spot",

			"id":  "4b465402-0f46-4e4f-b517-d4f2fada4e36",

			"image_link":  "https://storage.googleapis.com/tomkits/images/35c6b486-a329-4aac-bbe4-e1b26a6a3d85.jpg"},

			{

			"disease_name":  "Leaf_Mold",

			"id":  "6b1dc5a9-131e-4b31-99d8-674b72d4121b",

			"image_link":  "https://storage.googleapis.com/tomkits/images/62baa2d6-711a-43eb-a4c0-f941f03631db.jpg"}

			]

			}
    ```


**Authorization:**  
Bearer Token  
`<token>`

----------

### **GET**  -  **Prediction Detail by ID**

**Endpoint:**  
`GET http://34.50.72.127/predict/history/{prediction_id}`

**Description:**  
This endpoint provides the details of a specific prediction, including the disease name, confidence level, prediction time, and image URL.
**Responses:**

-   **200 OK**  
    Success:
    ```json
	{
	"confidence":  "98.74%",

	"description":  "Leaf mold is caused by the fungus Passalora fulva, and it affects the leaves, causing them to turn yellow and become moldy.",

	"disease_name":  "Leaf_Mold",

	"id":  "0cddea8a-0a4d-417c-b7d4-a9a6e27005a5",

	"image_link":  "https://storage.googleapis.com/tomkits/images/1e82a7f3-165d-4e56-8233-e2fc80a0e059.jpg",

	"product_list":  [

	{

	"active_ingredient":  "Propamocarb Hydrochloride",

	"product_image":  "https://storage.googleapis.com/tomkits/product/Previcur.png",

	"product_link":  "",

	"product_name":  "Previcur Flex"

	},

	{

	"active_ingredient":  "Chlorothalonil",

	"product_image":  "https://storage.googleapis.com/tomkits/product/Daconil_Fungicide.png",

	"product_link":  "",

	"product_name":  "Daconil Fungicide"

	},

	{

	"active_ingredient":  "Bacillus subtilis",

	"product_image":  "https://storage.googleapis.com/tomkits/product/Serenade_Garden.png",

	"product_link":  "",

	"product_name":  "Serenade Garden"

	}

	],

	"solution":  "Improve air circulation around the plants, prune affected leaves, and apply fungicides like azoxystrobin."

	}
    ```

**Authorization:**  
Bearer Token  
`<token>`
