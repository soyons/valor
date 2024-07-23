function getQueryParam(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

$(document).ready(function(){
    $('#filterExpressButton').click(function(){
        
        let sku = getQueryParam('sku');
        let shoename = getQueryParam('shoename');
        
        let filter = $(this).is(':checked') ? "EXPRESS" : "ALL"
        $.ajax({
            url: "/shoefilterExpressData",
            type: "get",
            data: {filter: filter, sku: sku, shoename: shoename},
            success: function(response) {
                console.log(response);
                let sales_data = response[0];
                let shoename = response[1];
                console.log(`filter datashoe name is ${shoename}`)

                let html = `<tr>
                    <th>Price</th>
                    <th>Size</th>
                    <th>Time</th>
                    <th>OrderType</th>
                </tr>`; // 用来存放新数据生成的html字符串

                // 遍历每一行数据
                for(let i=0; i < sales_data.length; i++) {
                    let row = sales_data[i];
                    // 使用模板字符串生成html
                    html += `<tr>
                                <td>${row['price']}</td>
                                <td>${row['size']}</td>
                                <td>${row['time']}</td>
                                <td>${row['orderType']}</td>
                            </tr>`;
                }
                console.log(html);
                $('.table-container table').html(html);
                $('#shoe-name').html(shoename); 
            },
            error: function(xhr) {
                //处理错误
                $('.table-container').html("<p>出了点问题，无法加载数据。请重试。重试有问题请联系管理员<p>"); 
            }
        });
    });
});