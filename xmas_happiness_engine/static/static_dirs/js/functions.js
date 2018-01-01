/* ===================================================================
 * Functions to call JS
 *
 * ------------------------------------------------------------------- */
 /* VueJS Settings */
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
  axios.defaults.xsrfCookieName = 'csrftoken'
  // register modal component
    Vue.component('modal', {
      template: '#modal-template'
    })
  /* VueJS Creating memory
	* ------------------------------------------------------ */
	var ssCreateMemory = function(input, create, mem_id) {

        var EngineRoot = 'http://' + window.location.hostname + ':' + window.location.port
        var APIinput = input.replace(/ /gi, "-");

        if (create == true) {
            var tht2memApi = EngineRoot + '/ttm/' + APIinput
        } else {
            var tht2memApi = EngineRoot + '/dbtm/' + mem_id
        }



        document.getElementById('homeinput').style.display = 'none';
        document.getElementById('notes').style.display = 'none';
        document.getElementById('new_memory').style.display = 'block';
        $("body").css("background-repeat", "repeat-y");

        var vueNewMemory = new Vue({
          delimiters: ['[[', ']]'],
          el: '#new_memory',
          data: {
            memory: [],
            errors: [],
            fault: false,
            menu: false,
            },
          mounted () {
            var self = this
            self.memory = APIinput
            axios.get(tht2memApi).then(response => {
              // JSON responses are automatically parsed.
              this.memory = response.data
              this.menu = true
            })
            .catch(e => {
              this.errors.push(e)
              this.fault = true
            })
          },
        })
    };
    /* ------------------------------------------------------ */
    /* VueJS writing notes
	* ------------------------------------------------------ */

    function textAreaAdjust(blog) {
          blog.style.height = blog.scrollHeight+"px";
      }

	var ssWriteNotes = function(linked, mem_id) {

	    console.log(linked)
	    console.log(mem_id)

        var EngineRoot = 'http://' + window.location.hostname + ':' + window.location.port
        var NotesAPI = EngineRoot + '/notes'
        var postNote = EngineRoot + '/newnote'

        document.getElementById('homeinput').style.display = 'none';
        document.getElementById('new_memory').style.display = 'none';
        document.getElementById('notes').style.display = 'block';
        $("body").css("background-repeat", "repeat-y");

        var vueNotes = new Vue({
          delimiters: ['[[', ']]'],
          el: '#notes',
          data: {
            notes: [],
            errors: [],
            fault: false,
            blogText: '',
            blogTitle: '',
            user: '',
            title: '',
            text: '',
            showModal: false,
            },
          created () {
            var self = this
            axios.get(NotesAPI).then(response => {
              this.notes = response.data
            })
            .catch(e => {
              this.errors.push(e)
              this.fault = true
            })
          },
          methods: {
            postNewNote () {
                var self = this
                axios.post(postNote, {
                    text: this.blogText,
                    title: this.blogTitle,
                })
                .then(response => {
                    swal({
                      title: 'Note posted',
                      type: 'success',
                      showCancelButton: false,
                      showConfirmButton: false
                    })
                    this.blogTitle = ''
                    this.blogText = ''
                    document.getElementById('newNoteText').style.height = '10rem';
                    axios.get(NotesAPI).then(response => {
                        this.notes = response.data
                    }).catch(e => {
                        this.errors.push(e)
                        this.fault = true
                    })
                })
                .catch(e => {
                  this.errors.push(e)
                  swal({
                      title: 'Error in posting note',
                      type: 'error',
                      showCancelButton: false,
                      showConfirmButton: false
                    })
                  this.blogTitle = e.response.data.title,
                  this.blogText = e.response.data.text
                })
            },
            itemClicked: function(item) {
                this.user = item.user
                this.title = item.title
                this.text = item.text
                this.showModal = true
            }
          }
        })
        };
