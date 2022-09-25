package requests

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"kitescratch/auth"
	"kitescratch/state"
	"kitescratch/ui"
	"net/http"
	"time"
)

type HTTPRequest struct {
	Method      string
	Url         string
	Data        any // A struct to send as JSON
	Body        []byte
	Headers     http.Header // Any custom headers
	Auth        *auth.Auth
	ErrorOnFail bool
	Reason      string
}

func (req HTTPRequest) String() string {
	return fmt.Sprintf("%s %s (reason: \"%s\", errorOnFail: %t)", req.Method, req.Url, req.Reason, req.ErrorOnFail)
}

func Request(req HTTPRequest) ([]byte, error) {
	if req.Reason == "" {
		req.Reason = "unknown"
	}
	ui.YellowText(req.String())

	cli := http.Client{
		Timeout: 10 * time.Second,
	}

	if req.Headers == nil {
		req.Headers = make(http.Header)
	}

	if req.Data != nil {
		// JSON serialize the data
		dataBytes, err := json.Marshal(req.Data)
		if err != nil {
			return nil, err
		}
		req.Body = dataBytes

		if v, ok := req.Headers["Content-Type"]; ok {
			ui.RedText("Not changing Content-Type from ", v, " to application/json")
		} else {
			req.Headers["Content-Type"] = []string{"application/json"}
		}
	}

	if req.Auth != nil {
		req.Headers["Frostpaw-Auth"] = []string{req.Auth.String()}
	}

	r, err := http.NewRequest(req.Method, state.GlobalState.BaseURL+req.Url, bytes.NewBuffer(req.Body))

	if err != nil {
		return nil, err
	}

	for k, v := range req.Headers {
		r.Header[k] = v
	}

	resp, err := cli.Do(r)

	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	if resp.StatusCode >= 400 && req.ErrorOnFail {
		return nil, fmt.Errorf("Request failed with status code %d", resp.StatusCode)
	}

	if resp.ContentLength > 0 {
		output := make([]byte, resp.ContentLength)
		_, err = io.ReadFull(resp.Body, output)
		if err != nil {
			return nil, err
		}

		if resp.StatusCode >= 400 {
			ui.YellowText("Request failed!\nStatus code:", resp.StatusCode, "\nBody:", string(output))
		}

		return output, nil
	}

	return []byte{}, nil
}

func RequestToStruct(req HTTPRequest, output any) {
	data, err := Request(req)
	if err != nil {
		ui.FatalText(err)
	}

	err = json.Unmarshal(data, output)
	if err != nil {
		ui.FatalText(err)
	}
}
