function Footer(course, term, univ, site) {
    this.course = course;
    this.term = term;
    this.university = univ;
    this.website = site;

    this.writeFooter = function() {
        document.write("<hr>")
        document.write("<p" + "class=\"footer\">Developed by: The Oklahoma Baptist University CIS departmentl, ")
        document.write(this.course + "--" + this.term + ", <a href=\"" + this.website + "\" target=\"_blank\">" + this.university + 
                      "</a>, page last modified: " + document.lastModified + "</p>")
        document.write("<br>")
        document.write("<p" + "class=\"footer-small\">Questions? Contact us at: <a href=\"mailto:cis-insiders@okbu.edu\">cis-insiders@okbu.edu</a></p>")
    }
}

newFooter = new Footer("CIS-4203", "Spring 2022", "Oklahoma Baptist University", "http://www.okbu.edu")
newFooter.writeFooter()