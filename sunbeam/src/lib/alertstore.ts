import { writable } from 'svelte/store';
import type { AlertType, AlertInputType } from './enums/enums';

interface AlertInputInterface {
  label: string;
  placeholder: string;
  multiline: boolean;
  required?: boolean;
  minlength: number;
  maxlength: number;
  multipleFiles?: boolean;
  type?: AlertInputType;
  description?: string;
  default?: string;
  id?: string; // Optional id
  validate?: (value) => string;
}

interface AlertButton {
  name: string;
  function: () => void;
}

interface Alert {
  title: string;
  type?: AlertType;
  message: string;
  id: string;
  show: boolean;
  icon: string;
  close?: () => void;
  submit?: (value) => void;
  inputs?: AlertInputInterface[];
  buttons?: AlertButton[];
}

type AlertStore = Alert;

export default writable<AlertStore>();

export const errorStore = writable<boolean>();
