from rest_framework_csv.renderers import CSVRenderer

class CSVResultsRenderer(CSVRenderer):
    def tablize(self, data):
        data = data['results']
        if data:
            header  = data['sets'].items()
            results = data['results']

            header_row = []
            values_row = []
            for (key, field) in header:
                header_row.append(field['title'])
                values_row.append(results[key])

            return [ header_row, values_row ] 

        else:
            return super(CSVResultsRenderer, self).tablize(data)


