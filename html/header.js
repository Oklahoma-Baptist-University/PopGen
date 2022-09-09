function Header(course, term, univ, site) {
    this.course = course;
    this.term = term;
    this.university = univ;
    this.website = site;

    this.writeHeader = function() {
        document.write("<title>CIS Insiders</title>")
        document.write("<link rel=\"shortcut icon\" href=\"assets/obu.ico\" type=\"image/x-icon\"/>")
        document.write("<link href=\"template.css\" type=\"text/css\" rel=\"stylesheet\"/>")
        document.write("<h1>OBU Stem Day</h1>")
        document.write("<div class=\"topnav\">")
            document.write("<a class=\"active\" href=\"template.html\">Home</a> ")
            document.write("<a href=\"blank.html\">About Us</a> ")
            document.write("<a href=\"blank.html\">Contact</a> ")
        document.write("</div>")
    }
}

newHeader = new Header("CIS-4203", "Spring 2022", "Oklahoma Baptist University", "http://www.okbu.edu")
newHeader.writeHeader()