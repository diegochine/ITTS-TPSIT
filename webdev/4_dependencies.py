from fastapi import FastAPI, Depends, HTTPException, status, Form
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse


class User(BaseModel):
    name: str
    pwd: str
    money: float = 0.0


app = FastAPI()
fake_users_db = {
    'travis': User(name='travis', pwd='nc17', money=7e7),
    'future': User(name='future', pwd='maskoff', money=3.6e6),
    'kendrick': User(name='kendrick', pwd='humble', money=43e6),
    'logic': User(name='logic', pwd='everybody', money=2.5e6),
}
current_user = None


@app.get('/')
async def root():
    return HTMLResponse("""<head>
        <style>
    .container {
      display: flex;
      justify-content: center;
    }
    .center {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
    }
    /* Bordered form */
    form {
      border: 3px solid #f1f1f1;
    }
    /* Full-width inputs */
    input[type=text], input[type=password] {
      width: 100%;
      padding: 12px 20px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      box-sizing: border-box;
    }
    /* Set a style for all buttons */
    button {
      background-color: #4CAF50;
      color: white;
      padding: 14px 20px;
      margin: 8px 0;
      border: none;
      cursor: pointer;
      width: 100%;
    }
    /* Add a hover effect for buttons */
    button:hover {
      opacity: 0.8;
    }
    /* Extra style for the cancel button (red) */
    .cancelbtn {
      width: auto;
      padding: 10px 18px;
      background-color: #f44336;
    }
    /* Center the avatar image inside this container */
    .imgcontainer {
      text-align: center;
      margin: 24px 0 12px 0;
    }
    /* Avatar image */
    img.avatar {
      width: 40%;
      border-radius: 50%;
    }
    /* Add padding to containers */
    .container {
      padding: 16px;
    }
    /* The "Forgot password" text */
    span.psw {
      float: right;
      padding-top: 16px;
    }
    /* Change styles for span and cancel button on extra small screens */
    @media screen and (max-width: 300px) {
      span.psw {
        display: block;
        float: none;
      }
      .cancelbtn {
        width: 100%;
      }
    }
    </style>
        </head>
        <body>
        <div class="container">
      	    <div class="center">
      		    <form action="/login" method="post">
      		    
    			<label for="username"><b>Username</b></label>
    			<input type="text" placeholder="Enter Username" name="username" required>

    			<BR>

    			<label for="password"><b>Password</b></label>
    			<input type="password" placeholder="Enter Password" name="password" required>

    			<BR>

    			<button type="submit">Login</button>
    		</form>
    		</div>
    	</div>
        </body>
        """)


@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    if username in fake_users_db and fake_users_db[username].pwd == password:
        global current_user
        current_user = username
        return RedirectResponse(url='/user/money', status_code=303)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@app.get("/logout")
async def logout():
    global current_user
    current_user = None
    return RedirectResponse(url='/', status_code=303)


@app.get("/user/", response_model=User)
async def get_current_user():
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in",
        )
    else:
        return current_user


@app.get("/user/money/")
async def get_money(user: User = Depends(get_current_user)):
    return {'message': f'you have {fake_users_db[user].money}$ in your bank account'}
