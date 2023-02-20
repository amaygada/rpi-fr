import React from 'react'

let baseURL = "https://241d-2405-201-17-f0cc-b498-3c83-3820-1a9c.ngrok.io/api/"

const filterFormField = [
  {
      "name": "Date",
      "id": "Date",
      "type": "date",
  }
]

class App extends React.Component{

  constructor(props){
    super(props)
    this.state = {
      data: [],
      date: ""
    }
  }

  getTemporalData = async () => {
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      let data = {
        "date": this.state.date
      }

      var raw = JSON.stringify(data);

      var requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
      };

      const response = await fetch(baseURL + "attend", requestOptions)
      return response.text()
  }

  apicall = async () => {
    let res = await this.getTemporalData()
    this.setState({data: JSON.parse(res).data})
  }

  render(){
    return(
      <>
        <div className=' w-full flex justify-between'>
            <h1 className='font-semibold text-lg sm:text-xl py-2 text-center md:text-4xl heading text-purple-600 mb-2'>
                Attendance
            </h1>
        </div>

        <br></br>
        <br></br>

        <div className='flex flex-wrap justify-center '>
          {filterFormField.map((data, key) => (
              <div className='flex flex-col p-2 border border-gray-600 rounded  m-2 w-1/3 '>
                  <h1 className='text-purplegray-900 mb-2'>{data.name}</h1>
                  <input
                      className='bg-purple-200 text-gray-700 appearance-none py-2 px-3 border rounded focus:bg-purple-50 focus:border-gray-400 focus:shadow-outline focus:outline-none'
                      type={data.type}
                      value={this.state.date}
                      onChange={e => this.setState({date: e.target.value})}
                  />
              </div>
          ))}
        </div>
        <div className="w-full my-3 flex justify-center">
            <button onClick={() => {this.apicall()}} className='bg-purple-600 px-7 py-2 text-white rounded-lg w-1/3'>Search</button>
        </div>

        <br></br>
        <br></br>

        <div class="flex flex-col mx-10">
            <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div class="py-2 inline-block min-w-full sm:px-6 lg:px-8">
                    <div class="overflow-hidden">
                        <table class="min-w-full">
                            <thead class="border-b">
                                <tr className='bg-purple-800 uppercase'>
                                    <th scope="col" class="text-sm font-medium  text-gray-100 px-6 py-4 text-left">
                                        #
                                    </th>
                                    <th scope="col" class="text-sm font-medium text-gray-100 px-6 py-4 text-left">
                                        Name
                                    </th>
                                    <th scope="col" class="text-sm font-medium text-gray-100 px-6 py-4 text-left">
                                        Email
                                    </th>
                                    <th scope="col" class="text-sm font-medium text-gray-100 px-6 py-4 text-left">
                                        time
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {this.state.data.map((data, key) => (
                                    <tr key={key} class="border-b">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                            {data.id}
                                        </td>
                                        <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                            {data.name}
                                        </td>
                                        <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                            {data.email}
                                        </td>
                                        <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                            {data.time}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
      </>
    )
  }
}

export default App;