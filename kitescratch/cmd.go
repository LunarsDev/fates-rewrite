package main

import (
	"fmt"
	"kitescratch/crypto"
	"kitescratch/ui"
	"strconv"
	"strings"
)

// The advanced tooling
type cmdError struct {
	Type     string
	ErrorVal error
	Success  bool
	LineNo   int
}

func (e cmdError) Error() string {
	return fmt.Sprintf("%s: %s", e.Type, e.ErrorVal)
}

func newCmdError(t string, e error, ln int) cmdError {
	return cmdError{
		Type:     t,
		ErrorVal: e,
		Success:  false,
		LineNo:   ln,
	}
}

func newCmdSuccess(msg string) cmdError {
	return cmdError{
		Type:     "Result",
		ErrorVal: fmt.Errorf(msg),
		Success:  true,
	}
}

func _handleEqualsSign(v []string) []string {
	vs := []string{}

	// EX: set a = 1 should become set a 1
	var hasSet bool
	for _, s := range v {
		if s == "=" && !hasSet {
			hasSet = true
			continue
		}
		vs = append(vs, s)
	}

	return vs
}

func _resolveVars(vMap map[string]string, v []string) []string {
	newV := []string{}
	for _, s := range v {
		if v, ok := vMap[s]; ok {
			newV = append(newV, v)
		} else {
			newV = append(newV, s)
		}
	}
	return newV
}

type Func struct {
	VarsMap map[string]string
	Code    []string
	CmdMap  map[string]Func // Function-specific commands
	Line    int
	Export  map[string]string
}

func newFunc() Func {
	return Func{
		VarsMap: map[string]string{},
		CmdMap:  map[string]Func{},
		Export:  map[string]string{},
	}
}

// Fset-able functions
var expMap = map[string]func(*Func, []string) string{
	"random": func(f *Func, args []string) string {
		if len(args) < 2 {
			args = append(args, "32")
		}

		i, err := strconv.Atoi(args[1])

		if err != nil {
			i = 32
		}

		return crypto.RandString(i)
	},
}

// Functions
var cmdMap = map[string]func(*Func, []string) cmdError{
	"http->get": func(f *Func, args []string) cmdError {
		return newCmdError("NotImplementedError", fmt.Errorf("GET not implemented"), f.Line)
	},
	"http->post": func(f *Func, args []string) cmdError {
		return newCmdError("NotImplementedError", fmt.Errorf("POST not implemented"), f.Line)
	},
	"set": func(f *Func, args []string) cmdError {
		args = _handleEqualsSign(args)
		if len(args) < 2 {
			return newCmdError("ArgumentError", fmt.Errorf("set requires 2 arguments"), f.Line)
		}

		newVal := strings.Join(_resolveVars(f.VarsMap, args[1:]), " ")

		f.VarsMap[args[0]] = newVal
		return newCmdSuccess(newVal)
	},
	"fset": func(f *Func, args []string) cmdError {
		args = _handleEqualsSign(args)
		if len(args) < 2 {
			return newCmdError("ArgumentError", fmt.Errorf("set requires 2 arguments"), f.Line)
		}

		newVals := _resolveVars(f.VarsMap, args[1:])

		for _, arg := range newVals {
			if v, ok := expMap[arg]; ok {
				f.VarsMap[args[0]] = v(f, newVals)
			}
		}

		return newCmdSuccess("fset done")
	},
	"func": func(f *Func, args []string) cmdError {
		if len(args) != 1 {
			return newCmdError("ArgumentError", fmt.Errorf("invalid args: func <name>"), f.Line)
		}

		var funcs []string

		for {
			inp := ui.AskInput("func " + args[0] + " [EOF to end]")
			if inp == "EOF" {
				break
			}
			funcs = append(funcs, inp)
		}

		fn := newFunc()
		fn.Code = funcs

		f.CmdMap[args[0]] = fn
		return newCmdSuccess(strings.Join(funcs, "\n"))
	},
	"export": func(f *Func, args []string) cmdError {
		if len(args) != 1 {
			return newCmdError("ArgumentError", fmt.Errorf("invalid args: export <name>"), f.Line)
		}

		if v, ok := f.VarsMap[args[0]]; ok {
			f.Export[args[0]] = v
			return newCmdSuccess(v)
		}

		return newCmdError("KeyError", fmt.Errorf("key %s not found", args[0]), f.Line)
	},
	"inf": func(f *Func, args []string) cmdError {
		var inf string

		for k, v := range f.VarsMap {
			inf += fmt.Sprintf("%s: %s", k, v)
		}

		for k, v := range f.CmdMap {
			inf += fmt.Sprintf("%s: %s", k, v.Code)
		}

		return newCmdSuccess(inf)
	},
}

var interpFunc = func(f *Func, args []string) cmdError {
	// Parse arguments
	f.VarsMap["test"] = "test"
	for i, code := range f.Code {
		if code == "" {
			continue
		}
		f.Line = i

		// Split the command
		args := strings.Split(code, " ")

		if len(args) < 1 {
			return newCmdError("ArgumentError", fmt.Errorf("not enough arguments"), f.Line)
		}

		if len(args) == 1 {
			// Local functions
			lf, ok := f.CmdMap[args[0]]

			if ok {
				err := cmdMap["_interp"](&lf, args[1:])
				if !err.Success {
					return err
				} else {
					for k, v := range lf.Export {
						// Export the variables
						f.VarsMap[k] = v
					}
					continue
				}
			} else {
				lf = *f
			}

			// Global functions
			fn, ok := cmdMap[args[0]]

			if ok {
				err := fn(f, args[1:])
				if !err.Success {
					return err
				} else {
					continue
				}
			}

			v, ok := f.VarsMap[args[0]]

			if !ok {
				return newCmdError("ArgumentError", fmt.Errorf("undefined variable %s", args[0]), f.Line)
			}

			return newCmdSuccess(v)
		}

		// Get the function
		fn, ok := cmdMap[args[0]]

		if !ok {
			return newCmdError("ArgumentError", fmt.Errorf("undefined command %s", args[0]), f.Line)
		}

		// Call the function
		err := fn(f, args[1:])

		if !err.Success {
			return err
		}

		if f.Line == len(f.Code)-1 {
			return err
		}
	}

	return newCmdSuccess("undefined")
}

func init() {
	cmdMap["_interp"] = interpFunc
}

func cmdView() {
	// Variables in cmdView

	f := newFunc()

	for {
		// Get the command
		cmd := ui.AskInput("CMD")

		// Split the command
		args := strings.Split(cmd, " ")

		f.Code = []string{cmd}

		// Call the interp function
		err := cmdMap["_interp"](&f, args[1:])

		if !err.Success {
			ui.RedText(err.Error())
		} else {
			ui.GreenText(err.Error())
		}
	}
}
