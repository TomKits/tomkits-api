## Dokumentasi API Tomkits

### **POST**  -  **Register**

**Endpoint:**  
`POST http://34.101.37.85:8000/auth/register`

**Deskripsi:**  
Endpoint ini digunakan untuk mendaftarkan pengguna baru ke dalam sistem. Pengguna harus menyediakan  `username`,  `email`, dan  `password`  untuk berhasil membuat akun.

**Request Body:**
```json
{
    "username": "Paulus Aditya Wicaksono",
    "email": "paulusaditya22@gmail.com",
    "password": "aditya1234"
}
```
**Responses:**

-   **201 Created**  
    Success:
```json
{ "message": "User registered successfully." }
```
**409 Conflict**  
Error (User already exists):
```json
{ "error": "User already exists" }
```

### **POST**  -  **User Login**

**Endpoint:**  
`POST http://34.101.37.85:8000/auth/login`

**Description:**  
This endpoint is used to authenticate an existing user. The user must provide a valid  `email`  and  `password`  to gain access.

**Request Body:**
```json
{
    "email": "paulusaditya22@gmail.com",
    "password": "aditya1234"
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

**Endpoint:**  
`GET http://34.101.37.85:8000/auth/whoami`

**Description:**  
This endpoint retrieves the information of the currently logged-in user based on the authentication token (JWT).

**Responses:**

-   **200 OK**  
    Success:
    ```json
	{

	"message":  "message",

	"user_details":  {

	"email":  "paulusaditya22@gmail.com",

	"username":  "Paulus Aditya Wicaksono"

	}

	}
    ```
    **Authorization:**  
Bearer Token  
`<token>`

### **POST**  -  **Refresh Access Token**

**Endpoint:**  
`POST http://34.101.37.85:8000/auth/refresh`

**Description:**  
This endpoint allows the user to refresh the authentication token using a valid refresh token.


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
`POST http://34.101.37.85:8000/auth/logout`

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
`POST http://34.101.37.85:8000/predict/disease`

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
	 **200 OK** - Prediction successful
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

### **GET**  -  **Prediction History**

**Endpoint:**  
`GET http://34.101.37.85:8000/predict/history`

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
`GET http://34.101.37.85:8000/predict/history/{prediction_id}`

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
