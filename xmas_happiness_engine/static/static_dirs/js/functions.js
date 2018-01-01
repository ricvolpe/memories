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
  var FIRST_CALL_mem = true
  var FIRST_CALL_note = true
  /* ----------------------------------------------------- */
  /* Reloading memories basic - CURRENTLY NOT USED
  * ------------------------------------------------------ */
  var ssNewMemory = function () {

        document.getElementById('homeinput').style.display = 'block'
        document.getElementById('notes').style.display = 'none'
        document.getElementById('new_memory').style.display = 'none'

  }
  /* ----------------------------------------------------- */
  /* VueJS Creating memory
  * ------------------------------------------------------ */
	var ssCreateMemory = function(input, create, mem_id) {

        var EngineRoot = 'http://' + window.location.hostname + ':' + window.location.port
        var APIinput = input.replace(/ /gi, "-");

        if (create == true) {var tht2memApi = EngineRoot + '/ttm/' + APIinput}
        else {var tht2memApi = EngineRoot + '/dbtm/' + mem_id}

        document.getElementById('homeinput').style.display = 'none'
        document.getElementById('new_memory').style.display = 'block'
        document.getElementById('notes').style.display = 'none'

        if (FIRST_CALL_mem == true) {
            vueNewMemory = new Vue({
              delimiters: ['[[', ']]'],
              el: '#new_memory',
              data: {
                memory: [],
                errors: [],
                create: create,
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
        } else {
        vueNewMemory.create = create
        vueNewMemory.memory = []
        vueNewMemory.errors = []
        vueNewMemory.fault = false
        vueNewMemory.menu = false
        axios.get(tht2memApi).then(response => {
          // JSON responses are automatically parsed.
          vueNewMemory.memory = response.data
          vueNewMemory.menu = true
        })
        .catch(e => {
          vueNewMemory.errors.push(e)
          vueNewMemory.fault = true
        })
        }
        FIRST_CALL_mem = false
    };
  /* ------------------------------------------------------ */
  /* VueJS writing notes
  * ------------------------------------------------------ */
    function textAreaAdjust(blog) {
          blog.style.height = blog.scrollHeight+"px";
      }

	var ssWriteNotes = function(linked, memId, thought) {

        var EngineRoot = 'http://' + window.location.hostname + ':' + window.location.port
        var NotesAPI = EngineRoot + '/notes'
        var postNote = EngineRoot + '/newnote'

        document.getElementById('homeinput').style.display = 'none';
        document.getElementById('new_memory').style.display = 'none';
        document.getElementById('notes').style.display = 'block';

        if (FIRST_CALL_note == true) {
            vueNotes = new Vue({
              delimiters: ['[[', ']]'],
              el: '#notes',
              data: {
                notes: [],
                errors: [],
                fault: false,
                blogText: '',
                blogTitle: thought,
                preLinked: linked,
                preMemId: memId,
                postLinked: false,
                postMemId: 0,
                user: '',
                title: '',
                text: '',
                showModal: false,
                },
              mounted() {
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
                        linked: this.preLinked,
                        memory_id: this.preMemId
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
                    this.postLinked = item.linked
                    this.postMemId = item.memory_id
                    this.showModal = true
                }
              }
            })
        } else {
        vueNotes.blogTitle = thought
        vueNotes.preLinked = linked
        vueNotes.preMemId = memId
        }
        FIRST_CALL_note = false
    };
