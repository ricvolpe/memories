/* ===================================================================
 * Functions to call JS
 *
 * ------------------------------------------------------------------- */
  /* VueJS Creating memory
	* ------------------------------------------------------ */
	var ssCreateMemory = function(input) {

        var EngineRoot = 'http://' + window.location.hostname + ':' + window.location.port
        var APIinput = input.replace(/ /gi, "-");
        var tht2memApi = EngineRoot + '/ttm/' + APIinput

        document.getElementById('homeinput').style.display = 'none';
        document.getElementById('new_memory').style.display = 'block';
        $("body").css("background-repeat", "repeat-y");

        var vueNewMemory = new Vue({
          delimiters: ['[[', ']]'],
          el: '#new_memory',
          data: {
            memory: [],
            errors: [],
            fault: false,
            },
          created () {
            var self = this
            self.memory = APIinput
            axios.get(tht2memApi).then(response => {
              // JSON responses are automatically parsed.
              this.memory = response.data
            })
            .catch(e => {
              this.errors.push(e)
              this.fault = true
            })
          },
        })
    };
    /* ------------------------------------------------------ */