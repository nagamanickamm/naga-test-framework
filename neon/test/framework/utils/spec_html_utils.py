import os

from naga.test.framework.utils.list_utils import ListUtils


class SpecHTMLUtils:

    def __create_html(spec_path, html_path):
        """create a HTML file for given spec file

        Args:
            spec_path (str): spec file path 
            html_path (str): html file path    
        """

        # Open Spec & HTML files
        specfile = open(spec_path)
        htmlfile = open(html_path, 'w+')
        Lines = specfile.readlines()

        # Set HTML header & Initialize variables
        htmlfile.writelines("<html><head></head><body>\n")
        step_done = False
        test_started = False
        table_not_added = True

        # Read every line from spec files
        for line in Lines:
            line = line.strip()

            # if line is a scenario
            if line.startswith('##'):
                if step_done:
                    htmlfile.writelines("<br></ul></blockquote></div>\n")
                htmlfile.writelines(
                    "<h3><span style=\"color:#3498db\"><span style=\"font-family:Comic Sans MS,cursive\"><span >{}</span></span></span></span></h3>\n"
                    .format(line.replace('##', 'Scenario => <span style=\"text-decoration:underline;border-bottom: 1px solid #000;\">')))
                test_started = True
                table_not_added = True

            # if line is a feature
            elif line.startswith('#'):
                htmlfile.writelines(
                    "<h1><span style=\"color:#27ae60\"><span style=\"font-family:Comic Sans MS,cursive\">{}</span></span></h1>\n".format(
                        line.replace('#', 'Feature => ')))

            # if line is a step
            elif line.startswith('*'):
                if not table_not_added:
                    htmlfile.writelines("</table></tbody>")
                    table_not_added = True
                if test_started:
                    htmlfile.writelines(
                        "<div><h4><span style=\"color:#8e44ad;margin: 35px;font-family:Georgia,serif;\"><u>Steps:</u></span></span></h4><blockquote style=\"background-color: #DFFADE; border-left: 8px solid #4ED849; width: 70%;\">"
                        + "<span style=\"font-family:Trebuchet MS,Helvetica,sans-serif\"><ul><br>\n")
                htmlfile.writelines(
                    "<li><span style=\"font-size:15px\"><span style=\"font-family:Courier New,Courier,monospace\"><span style=\"color:#2c3e50\">{}</span></span></span></li>\n"
                    .format(
                        line.replace('*', '').replace('<', "<strong style=\"color:#A10707;font-size:14px\"?").replace('>',
                                                                                                                      "</strong?").replace('?', '>')))
                step_done = True
                test_started = False

            # if line is a tag
            elif line.startswith('tag'):
                htmlfile.writelines(
                    "<p><span style=\"font-family:Trebuchet MS,Helvetica,sans-serif\"><span style=\"color:#999999\">{}</span></span></p>".format(
                        line))
                if not test_started:
                    htmlfile.writelines("<hr/>\n")

            # if line is a csv table
            elif line.startswith('table'):
                htmlfile.writelines(
                    "<p><span style=\"font-family:Trebuchet MS,Helvetica,sans-serif;margin: 35px;\"><span style=\"color:#A10707\">{}</span></span></p>"
                    .format(line))

            # if line is a underline or emty
            elif line == '' or line.startswith('===') or line.startswith('----') or '----' in line:
                pass

            # if line is a inline table
            elif '|' in line:
                if test_started and table_not_added:
                    htmlfile.writelines("<table style=\"width:500px;margin: 35px;\"><tbody>")
                htmlfile.writelines("<tr>")

                # Process data inside the table
                for cell in line.split('|'):
                    if test_started and table_not_added:
                        if cell != '':
                            htmlfile.writelines(
                                "<th style=\"border: 1px solid black; background-color:#D6EEEE; color:#A10707; font-size:16px border-style: dotted;text-align: center;\">&nbsp;{}</th>\n"
                                .format(cell))
                    else:
                        if cell != '':
                            htmlfile.writelines(
                                "<td style=\"border: 1px solid black;border-style: dotted;text-align: center;\">&nbsp;{}</td>\n".format(cell))
                table_not_added = False
                htmlfile.writelines("<tr>")
            else:
                htmlfile.writelines("<p>{}</p><br>\n".format(line))

        # Finish HTML file
        htmlfile.writelines("</body></html>\n")

    def convert_specs_html(spec_directory, html_directory):
        """Traverse through the spec folder and convert all spec to HTML file

        Args:
            spec_directory (str): spec folder path,  ex: os.getcwd()+'/test_suite/features/specs/'
            html_directory (str):html_path,  ex: os.getcwd()+'/features/'  
        """

        # Traverse through every directory under this path
        for files in os.walk(spec_directory):
            # Get all spec files under the directory
            reverse = list(reversed(files))
            spec_list = ListUtils.contains_partial_text(reverse[0], '.spec')

            # if spec file present
            if len(spec_list) > 0:
                folder_name = os.path.basename(files[0])
                path = files[0]

                # For each file in spec list
                for file_name in spec_list:
                    spec_path = path + '/' + file_name
                    feature_directory = html_directory
                    output_directory = feature_directory + folder_name
                    html_path = output_directory + '/' + file_name.replace('.spec', '.html')
                    #Create HTML directory based on spec directory
                    if not os.path.exists(feature_directory):
                        os.mkdir(feature_directory)
                    if not os.path.exists(output_directory):
                        os.mkdir(output_directory)
                    # Convert spec to HTML
                    SpecHTMLUtils.__create_html(spec_path, html_path)
