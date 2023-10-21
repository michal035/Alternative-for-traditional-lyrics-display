<script>

// Proper Docker Compose setup
// Untrack /migrations, __init__, admin.py, vscode, and __pycache__
// Clean up App.vue, create custom warning, outsource validating to a separate function 

import Modal from "./Modal.vue";

export default {
  name: "App",
  components: { Modal },

  data() {
    return {
      showModal: false,
      showModal_main: false,
      showModal_final: false,
      showmodal_first_page: false,
      showmodal_join_via_code: false,
      showmodal_create_code: false,
      showModal_set_code: false,
      showModalCreateNewUser: false,
      showPasswdDiv: false,
      showModalLogin: false,
      imgUrl: "",
      token: "",
      doc_url: "",
      email: null,
      //This is just for sake of validing data on client side while creating new account - sha256
      passwdTemp: null,
      passwdTempRe: null,
    };
  },

  methods: {
    validate() {
      var doc = document.querySelector('input[type="file"]');
      var file = doc.files[0];
      let extension = doc.value.split(".")[doc.value.split(".").length - 1];


      if (extension == "doc" || extension == "docx") {
        let f_size = file.size;
        f_size = f_size / 1000 / 1000;
        if (f_size > 500) {
          console.error("file is too big!");
        }
        this.setDoc(file);
      } else {
        
        console.error("Unaccepted file type");
      }
    },
    RedirectToPage_from_join_modal() {
      this.doc_url = "/" + document.getElementById("join_token").value;
      window.location.href = this.doc_url;
    },
    CloseModal(modalName) {
      this.showPasswdDiv = false;
      this[modalName] = false;
      location.reload();
    },
    OpenModal(modalNameToBeOpen, modalName = null, isFirst = false) {
      if (modalName != null) {
        this[modalName] = false;
      }
      this[modalNameToBeOpen] = true;

      if (isFirst == false) {
        location.reload();
      }
    },
    GetQR(token_) {
      const data = { token: token_ };
      const cookie = this.getCookie("bearerToken");


      const requestOptions = {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${cookie}`,
          },
        };

      fetch("http://127.0.0.1:8000/" + token_ + "/qr", requestOptions)
        .then((response) => response.blob())
        .then((blob) => {
          var imgUrl = URL.createObjectURL(blob);

          this.token = data.token;
          this.imgUrl = imgUrl;

          this.OpenModal("showModal_final",null,true)

          //this.showmodal_create_code = false;
          //this.showModal_final = true;
        })
        .catch((error) => console.error(error));
    },

    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
    },

    ShowInfo() {
      if (document.cookie) {
        const cookie = this.getCookie("bearerToken");

        console.log(cookie);
        this.showModal_main = false;

        var data = { code: "d" };

        const requestOptions = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${cookie}`,
          },
          body: JSON.stringify(data),
        };

        fetch("http://127.0.0.1:8000/create-new", requestOptions)
          .then((response) => response.json())
          .then((data) => {
            if (data.message) {

              this.showModalLogin = true;
            } else {
              this.GetQR(data.token);
            }
          });
      } else {
        console.error("Cookie not found")
        
        // New pop up - do you want to log in or create acc 
        this.showModalLogin = true;
      }
    },
    notFound() {
      var the_doc = document.getElementById("main");
      the_doc.innerHTML = `<br><h3 id="no_token">No document associated with this token</h3><br><p>Contact the document owner or create your own document.</p>`;
    },
    unauthorizedFileChange() {
      var the_doc = document.getElementById("main");
      the_doc.innerHTML = `<br><h3 id="no_token">You do not have permission to modify this file</h3><br><p>Contact the document owner or create your own document.</p>`;
    
      setTimeout(() => {
        this.RedirectToPage(); 
      }, 3000);
        
    },

    setDoc(file) {
      
      const formData = new FormData();
      formData.append('file', file);

      const data = { token: this.token };
      const cookie = this.getCookie("bearerToken");

      const requestOptions = {
          method: "POST",
          headers: {
            Authorization: `Bearer ${cookie}`,
          },
          body: formData
        };
      
      fetch("http://127.0.0.1:8000/upload/" + this.token + "/", requestOptions)
      .then(response => {
          if(response.ok){
              return response.json();
          }
          throw new Error('Network response was not ok.');
      })
      .then(data => {
          console.log(data); 
          this.RedirectToPage(); 
      })
      .catch(err => {
          console.error('Lack of perimissions', err);
          this.showModal = false;
          this.unauthorizedFileChange(); 
      });

    },


    GetQR_settings(token_) {
      
      const data = { token: token_ };
      const cookie = this.getCookie("bearerToken");

      const requestOptions = {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${cookie}`,
          },
        };

      fetch("http://127.0.0.1:8000/" + token_ + "/qr", requestOptions)
        .then((response) => response.blob())
        .then((blob) => {
          var imgUrl = URL.createObjectURL(blob);

          this.token = data.token;
          this.imgUrl = imgUrl;
        })
        .catch((err) => console.error(err));
    },
    ShowSettings() {
      this.showModal = true;
      const path = window.location.pathname;
      var token = path.substring(1);

      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      };

      this.GetQR_settings(token);
    },
    RedirectToPage() {
      this.doc_url = "/" + this.token;
      window.location.href = "/" + this.token;
      this.GetQR_settings(this.token);
    },

    // validations needs to be moved to seperate functon - login/create use to same part
   login() {
      const passwd = this.passwdTemp;
      if (passwd) {
        let regex = /@.*\./;
        if (!regex.test(this.email)) {
          document.getElementById("error-message").innerHTML = "Invalid email";
        } else {
          // There is HTTPS connection, but still I don't want for the actual password to leave to client
          const encoder = new TextEncoder();
          const data = encoder.encode(passwd);

          crypto.subtle
            .digest("SHA-256", data)
            .then((hashBuffer) => {
              var hashArray = Array.from(new Uint8Array(hashBuffer));
              var hashHex = hashArray
                .map((byte) => byte.toString(16).padStart(2, "0"))
                .join("");

              var data = {
                username: this.email,
                password: hashHex,
              };

              const requestOptions = {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
              };

              fetch("http://127.0.0.1:8000/login", requestOptions)
                .then((serverPromise) => {
                  if (serverPromise.ok) {
                    serverPromise.json().then((response) => {
                      document.cookie = `bearerToken=${response.token}`;
                      this.CloseModal("showModalLogin");
                      //this.ShowInfo();
                    });
                  } else {
                    document.getElementById("error-message").innerHTML =
                      "Invalid credentials";
                  }
                })
                .catch((error) => {
                  console.error("Error", error);
                });
            });
        }
      } else {
        document.getElementById("error-message").innerHTML = "Password is required";
      }
    },
    //Vaidations needs to be outsorced to seperate function 
    createNewUser() {
      const passwd = this.passwdTemp;
      if (passwd) {
        if (passwd != this.passwdTempRe) {
          console.error("passwords do not match");
          document.getElementById("error-message").innerHTML =
            "Passwords do not match";
        } else {
          let regex = /@.*\./;
          if (!regex.test(this.email)) {
            document.getElementById("error-message").innerHTML =
              "Invalid email";
          } else {
            // There is HTTPS connection, but still I don't want for the actual password to leave to client
            const encoder = new TextEncoder();
            const data = encoder.encode(passwd);

            crypto.subtle
              .digest("SHA-256", data)
              .then((hashBuffer) => {
                var hashArray = Array.from(new Uint8Array(hashBuffer));
                var hashHex = hashArray
                  .map((byte) => byte.toString(16).padStart(2, "0"))
                  .join("");

                var data = {
                  username: this.email,
                  password: hashHex,
                };

                const requestOptions = {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify(data),
                };

                fetch(
                  "http://127.0.0.1:8000/create-account",
                  requestOptions
                ).then((response) => {
                  this.showModalCreateNewUser = false;
                  return response;
                });
              })
              .catch((error) => {
                console.error("Error", error);
                console.log(response);
              });
          }
        }
      } else {
        document.getElementById("error-message").innerHTML =
          "Password is required";
      }
    },
  },
  mounted() {
    const path = window.location.pathname;
    var token = path.substring(1);

    fetch("http://127.0.0.1:8000/" + token)
      .then((response) => {
        if (response.status == 200) {
          return response.json();
        } else if (response.status === 404) {
          this.OpenModal("showModal_main", null, true);
          throw new Error("Resource not found");
        } else if (response.status === 204) {
          this.notFound();
          //Custom Warning needed
          throw new Error("There is no such .docx");
        } else {
          throw new Error("Something went wrong");
        }
      })
      .then((data) => {
        var tab = "<br><div id='con'>";
        console.log(data);

        console.log(data[2]["paragraph"]);

        for (let i = 0; data.length > i; i++) {
          let row = data[i]["paragraph"];
          if (row == "") {
            tab += "<br>";
          } else {
            tab += "<p style='text-align: center'>" + row + "</p>";
          }
        }

        tab += "</div>"
        var the_doc = document.getElementById("main");
        the_doc.innerHTML = tab;
      })
      .catch((error) => {
        console.error(error);
      });
  },
};
</script>



<template>
    <div id="app">
        <div class="settings-button" @click="ShowSettings">
            <i class="fas fa-cog"></i>
        </div>

        <!--First modal the user would see -->
        <Modal v-if="showModal_main">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" id="main_page" style="background: transparent; width: 50%">
                <div class="modal-content" style="background: transparent;" id="the_content_part" >
                    

                    <div class=" d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 custom-btn " style="width: 45%; margin: 20px;" @click="ShowInfo">Create new</button>
                        <button class="btn btn-dark btn-lg px-4 custom-btn " style="width: 45%; margin: 20px;" @click="OpenModal('showmodal_join_via_code','showModal_main', true)">Join via code</button>
                    </div>
                </div>
                    
            </div>     
        </Modal>



        <!-- Create account in modal - to be implemnted-->
        <Modal v-if="showModalCreateNewUser">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" style="width:100%" >
                <div class="modal-content" id="the_content_part" style="width:100%">
                    <div class="d-flex justify-content-center mt-4 col-md-6" style="width:100%">
                        <div>
                            <input v-model="email" class="form-control outline-danger outline_ custom-input" placeholder="Type in the email" type="text" id="email">
                            <br>
                            <input v-model="passwdTemp" class="form-control outline-danger outline_" placeholder="Type in the password" type="password" id="passwd">
                            <br>
                            <input v-model="passwdTempRe"  class="form-control outline-danger outline_" placeholder="Retype in the password" type="password" id="passwd">
                            <br>
                            <button class="btn btn-dark btn-lg px-4  " @click="createNewUser">Submit</button>
                        </div>
                          
                    </div>
                    <br>
                    <p id="error-message"></p>
                </div>
                
            </div>
        </Modal>



        <!-- Login account in modal-->
        <Modal v-if="showModalLogin">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" style="width:100%" >
                <div class="modal-content" id="the_content_part" style="width:100%">
                    <div class="d-flex justify-content-center mt-4 col-md-6" style="width:100%">
                        <div>
                            <!-- Further styling is needed-->
                            <input v-model="email" class="form-control outline-danger login-input-outline  outline__" placeholder="Type in the email" type="text" id="email">
                            <br>
                            <input v-model="passwdTemp" class="form-control outline-danger login-input-outline outline__" placeholder="Type in the password" type="password" id="passwd">
                            <br>
                            <button class="btn btn-dark btn-lg px-4 login-btn " @click="login">Login</button>
                        </div>
                    </div>
                    <br>
                    <p id="error-message"></p>
                </div>
                
            </div>
        </Modal>


        <!-- Final pop up after the creation 
            This is fine no need to change this 
        -->
        <Modal v-if="showModal_final">
            
                
                <div class="modal-body d-flex flex-column align-items-center background: transparent; width: 50%" style="width: 100%">
                            <br>

                            <div style="text-align: center; color: white;">
                               Here is the code:
                              <h3>{{ this.token }}</h3>
                            </div>
                           
                            <br>
                            <img :src=this.imgUrl onclick="downloadFile('${imgUrl}')">
                            <br>
                            <div style="text-align: center;">
                                <a :href=this.imgUrl download style="text-decoration: none; margin:20px;">
                                    <i class="fas fa-download" style="font-size: 40px; color: white; "></i> 
                                </a>

                                <a href="#" @click="OpenModal('showmodal_create_code','showModal_main')" style="text-decoration: none; margin:20px;">
                                    <i class="fas fa-lock" style="font-size: 40px; color: white; "></i> 
                                </a>


                                  <a :href=this.doc_url @click="RedirectToPage" style="text-decoration: none; margin:20px;">
                                    <i class="fas fa-window-close" style="font-size: 40px; color: white; "></i>
                                </a>

                            </div>

                </div>
                       
        </Modal>                                 

        <!--  
            This is main settings pop up - there needs to be a login option
        -->
        <Modal v-if="showModal">
            
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" style="background: transparent; width: 50%">
                <div class="modal-content" id="the" style="background: transparent;" >
                    
                    <div v-if="showPasswdDiv" class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" placeholder="Type in the code " type="text" id="the_code_r">
                    </div>
                    
                    <br>

                    <div class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" type="file"  id="the_file">
                    </div>
                    <div class="modal-footer d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="validate">Save</button>
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="CloseModal('showModal')">Close</button>
                    </div>
                    <br>
                    <br>
                    <div>
                    <div id="qrcode"></div>
                        <img :src=this.imgUrl onclick="downloadFile('${imgUrl}')">
                    </div>
                    
                </div>
                    
            </div>

        </Modal>

 
        <!-- Create the code  
        
        -->
        <Modal v-if="showmodal_create_code">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable"  style="background: transparent; width: 50%">
                <div class="modal-content" style="background: transparent;" >

                    <div class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" placeholder="Type in the code - this will alow you to make changes, treat this like a password" type="text" id="the_passwd">
                    </div>
                                   
                    <div class="modal-footer d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="SetPasswd">Create</button>
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="CloseModal('showmodal_create_code')">Close</button>
                    </div>                
                </div>
            </div>     
        </Modal>


        <!-- Join via code modal -->

        <Modal v-if="showmodal_join_via_code">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" style="background: transparent; width: 50%">
                <div class="modal-content" style="background: transparent;"  >
                    
                    <div class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" placeholder="Type in the token" type="text" id="join_token">
                    </div>
                                
                    <div class="modal-footer d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="RedirectToPage_from_join_modal">Join</button>
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="CloseModal('ShowModal')">Close</button>
                    </div>                
                      
                </div>
            </div>     
        </Modal> 


        <div>
            <div class="a" id="main"></div>
        </div>
    </div>
</template>