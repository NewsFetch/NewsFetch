import React from "react";
import {
    ReactiveBase,
    DataSearch,
    MultiList,
    ReactiveList,
    ResultList
} from "@appbaseio/reactivesearch";

const { ResultListWrapper } = ReactiveList;

function App() {
    return (
        <ReactiveBase
            url="http://localhost:9200"
            app="newsfetch"
        >
            {/* other components will go here. */}
            <div style={{ display: "flex", flexDirection: "row" }}>
                <div
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        width: "30%",
                        margin: "10px"
                    }}
                >
                    <MultiList
                        componentId="authorsfilter"
                        dataField="authors.keyword"
                        title="Filter by Authors"
                        aggregationSize={5}
                    />
                    {/*}
                    <SingleRange
                        componentId="ratingsfilter"
                        dataField="average_rating"
                        title="Filter by Ratings"
                        data={[
                            { start: 4, end: 5, label: "4 stars and above" },
                            { start: 3, end: 5, label: "3 stars and above" },
                            { start: 1, end: 5, label: "Any ratings" }
                        ]}
                        defaultValue="4 stars and up"
                    />
                    */}
                </div>
                <div style={{ display: "flex", flexDirection: "column", width: "66%" }}>
                    <DataSearch
                        style={{
                            marginTop: "35px"
                        }}
                        componentId="searchbox"
                        dataField={[
                            "title",
                            "title.autosuggest",
                        ]}
                        fieldWeights={[3, 1]}
                        placeholder="Search for articles"
                    />
                    <ReactiveList
                        componentId="results"
                        dataField="title"
                        size={6}
                        pagination={true}
                        react={{
                            and: ["searchbox", "authorsfilter"]
                        }}
                        style={{ textAlign: "center" }}
                        render={({ data }) => (
                            <ResultListWrapper>
                                {data.map((item) => (
                                    <ResultList key={item._id}>
                                        <ResultList.Content>
                                            <ResultList.Title
                                                dangerouslySetInnerHTML={{
                                                    __html: item.title
                                                }}
                                            />
                                            <ResultList.Description>
                                                <div>
                                                    <div>by {item.content}</div>
                                                    <div>
                                                        ({item.authors})
                                                    </div>
                                                </div>
                                            </ResultList.Description>
                                        </ResultList.Content>
                                    </ResultList>
                                ))}
                            </ResultListWrapper>
                        )}
                    />
                </div>
            </div>
        </ReactiveBase>
    );
}

export default App;